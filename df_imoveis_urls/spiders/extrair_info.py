import scrapy
import re
import pandas as pd

class ExtrairInfoSpider(scrapy.Spider):

    # COMANDO PARA EXECUTAR A SPIDER:
    #
    #   scrapy crawl extrair_info -o resultados/imoveis.csv

    name = "extrair_info"

    allowed_domains = ["www.dfimoveis.com.br"]
    
    df = pd.read_csv("./json_txt/links_imoveis.txt", header=None, names=["links"]) 
    start_urls = df["links"].tolist()

    def parse(self, response):
            
            telefone_whatsapp = response.css("a.FalarComOAnunciantePeloWhatsapp::attr(data-link)").get() #whatsapp
            # telefone = re.search(r"phone=(\d+)", telefone_whatsapp).group(1) if telefone_whatsapp else "Não informado" #whatsapp          
            # telefone_parte1 = response.css('span.teaser a span::text').get().strip()
            # telefone_parte2 = response.css('a.telefone_anunciante.complete::text').get().strip()
            # telefone_completo = f"{telefone_parte1}{telefone_parte2}"

            telefone = re.search(r"phone=(\d+)", telefone_whatsapp).group(1) if telefone_whatsapp else ""  # WhatsApp          
            telefone_parte1 = (response.css('span.teaser a span::text').get() or "").strip()
            telefone_parte2 = (response.css('a.telefone_anunciante.complete::text').get() or "").strip()

            # Criar o telefone completo apenas se houver algum valor
            telefone_completo = f"{telefone_parte1}{telefone_parte2}".strip()
            telefone_completo = telefone_completo if telefone_completo else "Não informado"



            yield {
                
                "cidade": response.css("h6:contains('Cidade:') small::text").get(default="Não informado").strip(),
                "bairro": response.css("h6:contains('Bairro:') small::text").get(default="Não informado").strip(),
                "endereco": response.css("h1.mb-0.font-weight-600.mobile-fs-1-5::text").get(default="Não encontrado").strip(),
                "quartos": response.css("h6:contains('Quartos:') small::text").get(default="0").strip(),
                "suites": response.css("h6:contains('Suítes:') small::text").get(default="0").strip(),
                "garagens": response.css("h6:contains('Garagens:') small::text").get(default="0").strip(),
                "posicao_sol": response.css(".row h6:contains('Posição do Sol:') small::text").get(default="Não encontrado").strip(),
                "area_util": response.css("h6:contains('Área Útil:') small::text").get(default="Não encontrado").strip(),
                "preco": response.css(".display-5.text-warning.precoAntigoSalao::text").get(default="Não encontrado").strip(),
                
                #Dados Vendedor
                "nome_vendedor": response.css("div.col-8.col-md-5 h6::text").get(default="Não informado").strip(),
                "creci": response.css("div.col-8.col-md-5 small::text").re_first(r"\d+", "Não informado"),
                "whatsapp": telefone,
                "Telefone": telefone_completo,
                
                #Detalhes
                "aceita_financiamento": response.css(".row h6:contains('Aceita Financiamento:') small::text").get(default="Não encontrado").strip(),
                
                "posicao_imovel": response.css(".row h6:contains('Posição do Imóvel:') small::text").get(default="Não encontrado").strip(),
                "nome_edificio": response.css(".row h6:contains('Nome do Edifício:') small::text").get(default="Não encontrado").strip(),
                "ultima_atualizacao": response.css(".row h6:contains('Última Atualização:') small::text").get(default="Não encontrado").strip(),
                "unidades_andar" : response.css(".row h6:contains('Unidades no Andar:') small::text").get(default="Não econtrado").strip(),
                "total_andares_empr" : response.css(".row h6:contains('Total de Andar do Empreendimento:') small::text").get(default="Não econtrado").strip(),
                "unidades_andar" : response.css(".row h6:contains('Unidades no Andar:') small::text").get(default="Não econtrado").strip(),

                #Descrição
                "descricao": [descricao.replace(";", "") for descricao in response.css("p.texto-descricao::text").getall()],
                "url_origem": response.url

            }