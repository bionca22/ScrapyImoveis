# Limpar dados obtidos no imoveis.csv

import pandas as pd
import numpy as np
import os
import re
import requests
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

arquivo_csv = os.path.join(PARENT_DIR, "resultados", "imoveis.csv") # (DIRETORIO, PASTA, ARQUIVO)

df = pd.read_csv(arquivo_csv)


# AREA UTIL E AREA TOTAL

df["area_util"] = df["area_util"].astype(str).replace("Não encontrado", np.nan).str.replace(r"\.", "", regex=True).str.strip()
df["area_util"] = df["area_util"].str.replace(" m²", "", regex=False).str.replace(",", ".")
df["area_util"] = df["area_util"].astype(float).map(lambda x: f"{x:.2f}")

df["area_total"] = df["area_total"].astype(str).replace("Não encontrado", np.nan).str.replace(r"\.", "", regex=True).str.strip()
df["area_total"] = df["area_total"].str.replace(" m²", "", regex=False).str.replace(",", ".")
df["area_total"] = df["area_total"].astype(float).map(lambda x: f"{x:.2f}")

df["total_andares_empr"] = df["total_andares_empr"].astype(str).replace("Não encontrado", np.nan).replace("Não econtrado", np.nan).str.replace(" Andares", "").str.replace(" Andar", "")
#print(df["total_andares_empr"].unique()) # debug para ver os valores únicos da coluna



# QUARTOS SUITES E GARAGENS

df["quartos"] = df["quartos"].astype(int)
df["suites"] = df["suites"].astype(int)
df["garagens"] = df["garagens"].astype(int)



#TELEFONES

def limpar_telefones(texto):
    
    if pd.isna(texto):
        return []

    texto = re.sub(r'[^0-9\(\)\-]', '', texto)
    telefones = re.findall(r"\(\d{2}\)\s?\d{4,5}-\d{4}", texto)

    return list(set(telefones))


df["telefone"] = df["telefone"].apply(limpar_telefones)

# print(df["telefone"].head(10))



# GOOGLE API (NÃO USAR PARA TESTAR COM O DATAFRAME INTEIRO)

load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

def get_address(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        return data['results'][0]['formatted_address']
    else:
        return "Endereço não encontrado"
    
# df["endereco_google"] = get_address(df["latitude"],df["longitude"])

latitude = df.loc[0, 'latitude']
longitude = df.loc[0, 'longitude']

endereco = (get_address(latitude, longitude))

print (endereco) #Qnp 5 Cj O Lt 8 - s/n lt 8 - Ceilândia, Brasília - DF, 72240-421, Brazil