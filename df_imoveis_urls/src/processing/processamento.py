import os
import numpy as np
import pandas as pd
import re

def limpar_area(df, coluna):
    df[coluna] = (
        df[coluna].astype(str)
        .replace("Não encontrado", np.nan)
        .str.replace(r"\.", "", regex=True)
        .str.strip()
        .str.replace(" m²", "", regex=False)
        .str.replace(",", ".")
        .astype(float)
        .map(lambda x: f"{x:.2f}" if not np.isnan(x) else np.nan)
    )

    return df
    
def limpar_telefones(texto):
    
    if pd.isna(texto):
        return []

    texto = re.sub(r'[^0-9\(\)\-]', '', texto)
    telefones = re.findall(r"\(\d{2}\)\s?\d{4,5}-\d{4}", texto)

    return list(set(telefones))

def formatar_caracteristicas(texto):
    if pd.isna(texto):
        return []
    return sorted([item.strip() for item in texto.split(",")])

def coletar_todas_caracteristicas(df, coluna):
    todas = set()
    for lista in df[coluna]:
        todas.update(lista)
    return sorted(todas)

def expandir_caracteristicas(df, coluna):
    df[coluna] = df[coluna].apply(formatar_caracteristicas)
    todas_caracteristicas = coletar_todas_caracteristicas(df, coluna)
    
    for caracteristica in todas_caracteristicas:
        df[caracteristica] = df[coluna].apply(lambda x: 1 if caracteristica in x else 0)

    df.drop(columns=[coluna], inplace=True)
    return df