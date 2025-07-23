import scrapy
import re
import json 
from pathlib import Path

class ExtrairInfoSpider(scrapy.Spider):

    name = "extrair_info"

    allowed_domains = ["www.dfimoveis.com.br"]
    
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data" / "raw"
    links_file = DATA_DIR / "links_imoveis.txt"

    #Leitura correta
    with open(links_file, 'r') as f:
        start_urls = [line.strip() for line in f]

    def parse(self, response):
            
            telefone_textos = response.css("h2.telefone *::text").getall()
            telefone_completo = " ".join(telefone_textos)
            telefone_formatado = re.sub(r"[^0-9()\-\s]", "", telefone_completo).strip()
            descricao_lista = [desc.replace(";", "") for desc in response.css("p.texto-descricao::text").getall()]
            

            yield {
                
                "id_dfi": re.search(r'ID:\s*(\d+)', response.css("title::text").get()).group(1),
                "cidade": response.css("h6:contains('Cidade:') small::text").get(default="Não encontrado").strip(),
                "bairro": response.css("h6:contains('Bairro:') small::text").get(default="Não encontrado").strip(),
                "endereco": response.css("h1.mb-0.font-weight-600.mobile-fs-1-5::text").get(default="Não encontrado").strip(),
                "quartos": response.css("h6:contains('Quartos:') small::text").get(default="0").strip(),
                "suites": response.css("h6:contains('Suítes:') small::text").get(default="0").strip(),
                "garagens": response.css("h6:contains('Garagens:') small::text").get(default="0").strip(),
                "posicao_sol": response.css(".row h6:contains('Posição do Sol:') small::text").get(default="Não encontrado").strip(),
                "area_util": response.css("h6:contains('Área Útil:') small::text").get(default="Não encontrado").strip(),
                "area_total": response.css(".row h6:contains('Área Total:') small::text").get(default="Não encontrado").strip(),
                "preco": response.css(".display-5.text-warning.precoAntigoSalao::text").get(default="Não encontrado").strip(),
                "características" : ", ".join(response.css("#detalhe-imovel ul.checkboxes li::text").getall()),
                "latitude": response.css("script::text").re_first(r"latitude\s*=\s*([-+]?\d*\.\d+)"),
                "longitude": response.css("script::text").re_first(r"longitude\s*=\s*([-+]?\d*\.\d+)"),
                
                #Dados Vendedor
                "nome_vendedor": response.css("div.col-8.col-md-5 h6::text").get(default="Não encontrado").strip(),
                "creci": response.css("div.col-8.col-md-5 small::text").re_first(r"\d+", "Não encontrado"),
                "whatsapp": response.css("a.FalarComOAnunciantePeloWhatsapp::attr(data-link)").re_first(r"phone=(\d+)&"),
                "telefone": telefone_formatado,
                "publicado_dias":response.css("h6:contains('Publicado há:') small::text").get(default="Não encontrado").strip(),
                
                #Detalhes
                "aceita_financiamento": response.css(".row h6:contains('Aceita Financiamento:') small::text").get(default="Não encontrado").strip(),
                "posicao_imovel": response.css(".row h6:contains('Posição do Imóvel:') small::text").get(default="Não encontrado").strip(),
                "nome_edificio": response.css(".row h6:contains('Nome do Edifício:') small::text").get(default="Não encontrado").strip(),
                "ultima_atualizacao": response.css(".row h6:contains('Última Atualização:') small::text").get(default="Não encontrado").strip(),
                "unidades_andar" : response.css(".row h6:contains('Unidades no Andar:') small::text").get(default="Não encontrado").strip(),
                "total_andares_empr" : response.css(".row h6:contains('Total de Andar do Empreendimento:') small::text").get(default="Não encontrado").strip(),
                "unidades_andar" : response.css(".row h6:contains('Unidades no Andar:') small::text").get(default="Não encontrado").strip(),

                #Descrição
                "descricao": json.dumps(descricao_lista, ensure_ascii=False),
            }