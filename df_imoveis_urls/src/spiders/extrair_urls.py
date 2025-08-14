import scrapy
from pathlib import Path
import os
from datetime import datetime

class ExtrairUrlsSpider(scrapy.Spider):
    name = "extrair_urls"
    
    base_url = "https://www.dfimoveis.com.br/venda/df/ceilandia/ceilandia-norte/casa"
    
    # Configuração de saída automática
    custom_settings = {
        'FEEDS': {
            'data/raw/urls_%(time)s.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
                'overwrite': True
            }
        }
    }

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse, meta={"pagina": 1})

    def parse(self, response):
        pagina = response.meta["pagina"]

        # Verifica se há a mensagem "Neste momento, não temos imóveis..."
        if mensagem := response.css("div.no-has-content h4::text").get():
            if "não temos imóveis" in mensagem:
                self.logger.info(f"Fim da raspagem: Página {pagina} não contém imóveis")
                return

        # Processa os links
        links_imoveis = [
            f"https://www.dfimoveis.com.br{link}" 
            for link in response.css("a::attr(href)").getall() 
            if link.startswith("/imovel/")
        ]

        yield {
            "pagina": pagina,
            "num_links": len(links_imoveis),
            "links": links_imoveis
        }

        # Chama a próxima página
        proxima_pagina = pagina + 1
        yield scrapy.Request(
            url=f"{self.base_url}?pagina={proxima_pagina}",
            callback=self.parse,
            meta={"pagina": proxima_pagina}
        )