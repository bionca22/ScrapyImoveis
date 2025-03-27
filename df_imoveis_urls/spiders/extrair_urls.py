import scrapy

class ExtrairUrlsSpider(scrapy.Spider):

    # COMANDO PARA EXECUTAR A SPIDER:
    #   
    #   scrapy crawl extrair_urls -o json_txt/urls.json && python json_txt/json_txt.py
    #
    #   Esse comando roda a spider "extrair_urls" e se não der erros, roda o script json_txt.py para criar o arquivo links_imoveis.txt
    

    name = "extrair_urls"
    
    base_url = "https://www.dfimoveis.com.br/venda/df/ceilandia/ceilandia-norte/casa"

    def start_requests(self):
        # Começa pela primeira página (sem "?pagina=")
        yield scrapy.Request(url=self.base_url, callback=self.parse, meta={"pagina": 1})

    def parse(self, response):
        pagina = response.meta["pagina"]

        # Verifica se há a mensagem "Neste momento, não temos imóveis..."
        mensagem = response.css("div.no-has-content h4::text").get()
        if mensagem and "não temos imóveis" in mensagem:
            self.log(f"Fim da raspagem: Página {pagina} não contém imóveis. Última página válida: {pagina - 1}")
            return  # Para a raspagem

        # Filtra apenas os links que começam com "/imovel/"
        links = response.css("a::attr(href)").getall()
        links_imoveis = [
            f"https://www.dfimoveis.com.br{link}" for link in links if link.startswith("/imovel/")
        ]

        # Salva os links encontrados na página atual
        yield {
            "pagina": pagina,
            "num_links": len(links_imoveis),
            "links": links_imoveis
        }

        # Chama a próxima página
        proxima_pagina = pagina + 1
        proxima_url = f"{self.base_url}?pagina={proxima_pagina}"
        yield scrapy.Request(url=proxima_url, callback=self.parse, meta={"pagina": proxima_pagina})
    
