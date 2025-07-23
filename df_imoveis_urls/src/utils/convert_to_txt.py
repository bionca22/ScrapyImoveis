import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
    #input_path = BASE_DIR / "data" / "raw" / "urls.json"

latest_file = max((BASE_DIR / "data" / "raw").glob("urls_*.json"), key=os.path.getmtime)
input_path = str(latest_file)
    
output_path = BASE_DIR / "data" / "raw" / "links_imoveis.txt"

def convert_json_to_txt():
    """Converte JSON de URLs para arquivo TXT, removendo duplicatas."""

    try:
        # Carrega e processa os dados
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Extrai links únicos mantendo a ordem
        unique_links = []
        seen = set()
        for item in data:
            for link in item.get("links", []):
                if link not in seen:
                    seen.add(link)
                    unique_links.append(link)
        
        # Salva os resultados
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(unique_links))
        
        print(f"✅ {len(unique_links)} links únicos salvos em {output_path}")

    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {input_path}")
    except json.JSONDecodeError:
        print(f"❌ Erro ao ler JSON em: {input_path}")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    convert_json_to_txt()