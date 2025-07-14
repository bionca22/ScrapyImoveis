import pandas as pd
import numpy as np
import os
import re
from .google_api import get_address
from .processamento import limpar_area, limpar_telefones, expandir_caracteristicas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data")  # Volta dois níveis
arquivo_csv = os.path.join(DATA_DIR, "raw", "resultados", "imoveis.csv")


df = limpar_area(df, "area_util")
df = limpar_area(df, "area_total")

df["total_andares_empr"] = df["total_andares_empr"].astype(str).replace("Não encontrado", np.nan).replace("Não econtrado", np.nan).str.replace(" Andares", "").str.replace(" Andar", "")

df["quartos"] = df["quartos"].astype(int)

df["suites"] = df["suites"].astype(int)

df["garagens"] = df["garagens"].astype(int)

#df["preco"] = df["preco"].astype(float)

df["telefone"] = df["telefone"].apply(limpar_telefones)

df = expandir_caracteristicas(df, "características") # Tranforma a lista para colunas binárias



# GOOGLE API (NÃO USAR PARA TESTAR COM O DATAFRAME INTEIRO)

# df["endereco_coordenadas"] = get_address(df["latitude"],df["longitude"])

latitude = df.loc[0, 'latitude'] # Pegar primeira linha para testes
longitude = df.loc[0, 'longitude']

#endereco = (get_address(latitude, longitude))

#print (endereco) #Qnp 5 Cj O Lt 8 - s/n lt 8 - Ceilândia, Brasília - DF, 72240-421, Brazil


# COLUNAS
#
# ['cidade', 'bairro', 'endereco', 'quartos', 'suites', 'garagens', 
# 'posicao_sol', 'area_util', 'area_total', 'preco', 'latitude', 'longitude', 
# 'nome_vendedor', 'creci', 'whatsapp', 'telefone', 'publicado_dias:', 'aceita_financiamento', 
# 'posicao_imovel', 'nome_edificio', 'ultima_atualizacao', 'unidades_andar', 'total_andares_empr', 
# 'titulo', 'descricao', 'url_origem', 

# CARACTERISTICAS (0,1)
# 'Aceita Pets', 'Aquecimento Solar', 'Ar Condicionado', 
# 'Cozinha Espaçosa', 'Cozinha com Armários', 'Despensa', 'Escritorio', 'Interfone', 'Jardim', 
# 'Lavabo', 'Mobiliado', 'Pintura Nova', 'Piscina', 'Piso em Porcelanato', 'Portão Eletrônico', 
# 'Projeto de Iluminação', 'Salão Gourmet', 'Salão de Festas', 'Sauna', 'Varanda', 'Vista Livre', 
# 'Área de Lazer', 'Área de Serviço', 'Área de Serviço Coberta']
