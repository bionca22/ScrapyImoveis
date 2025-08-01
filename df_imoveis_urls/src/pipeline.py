import os
import re
import json
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Configuração inicial
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# 1. Leitura dos dados raspados
def ler_dados_raspados():
    raw_dir = DATA_DIR / "raw" / "resultados"
    arquivos = list(raw_dir.glob("*.json"))
    
    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo de dados raspados encontrado")
    
    # Encontra o arquivo mais recente
    arquivo_recente = max(arquivos, key=os.path.getmtime)
    
    with open(arquivo_recente, 'r', encoding='utf-8') as f:
        dados = [json.loads(linha) for linha in f]
    
    return pd.DataFrame(dados)

# 2. Funções de processamento otimizadas
def limpar_valor_numerico(serie):
    return (
        pd.to_numeric(
            serie.replace("Não encontrado", np.nan)
            .str.replace(r"[^\d.,]", "", regex=True)
            .str.replace(".", "", regex=False)
            .str.replace(",", "."),
            errors='coerce'
        )
    )

def processar_telefones(telefones):
    if pd.isna(telefones) or not telefones:
        return []
    
    nums = re.findall(r"\(\d{2}\)\s?\d{4,5}-\d{4}", telefones)
    return list(set(nums))[:3]  # Limita a 3 telefones

def expandir_caracteristicas(df):
    todas_caracteristicas = set()
    df['caracteristicas'] = df['características'].str.split(',').apply(
        lambda x: [c.strip() for c in x] if isinstance(x, list) else []
    )
    
    for caracs in df['caracteristicas']:
        todas_caracteristicas.update(caracs)
    
    for carac in todas_caracteristicas:
        if carac:  # Ignora strings vazias
            df[f"carac_{carac}"] = df['caracteristicas'].apply(
                lambda x: 1 if carac in x else 0
            )
    
    return df.drop(columns=['caracteristicas', 'características'])

# 3. Conexão com Supabase
class SupabaseLoader:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client = create_client(self.url, self.key)
    
    def carregar_imoveis(self, df):
        # Converter DataFrame para dicionários
        registros = df.replace({np.nan: None}).to_dict('records')
        
        for registro in registros:
            try:
                # Converter listas para strings
                for chave in ['telefone', 'caracteristicas']:
                    if chave in registro and isinstance(registro[chave], list):
                        registro[chave] = ", ".join(registro[chave])
                
                # Inserção/atualização
                self.client.table('imoveis').upsert(
                    [registro],
                    on_conflict='id_dfi'
                ).execute()
            
            except Exception as e:
                print(f"Erro ao inserir ID {registro.get('id_dfi')}: {str(e)}")

# 4. Pipeline principal
def executar_pipeline():
    # Passo 1: Carregar dados
    df = ler_dados_raspados()
    
    # Passo 2: Limpeza e transformação
    df = df[[
        'id_dfi', 'cidade', 'bairro', 'endereco', 'quartos', 'suites', 
        'garagens', 'area_util', 'area_total', 'preco', 'latitude', 
        'longitude', 'nome_vendedor', 'creci', 'telefone', 'características'
    ]].copy()
    
    # Processar campos numéricos
    for coluna in ['quartos', 'suites', 'garagens']:
        df[coluna] = df[coluna].fillna(0).astype(int)
    
    for coluna in ['area_util', 'area_total', 'preco']:
        df[coluna] = limpar_valor_numerico(df[coluna])
    
    # Processar telefones e características
    df['telefone'] = df['telefone'].apply(processar_telefones)
    df = expandir_caracteristicas(df)
    
    # Passo 3: Carregar no banco
    loader = SupabaseLoader()
    loader.carregar_imoveis(df)
    
    print(f"✅ Pipeline concluído! {len(df)} registros processados.")

if __name__ == "__main__":
    executar_pipeline()