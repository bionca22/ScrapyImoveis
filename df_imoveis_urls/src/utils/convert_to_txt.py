import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#json_file
input_path = os.path.join("..", "..", "data", "raw", "urls.json")
#txt_file
output_path = os.path.join("..", "..", "data", "raw", "links_imoveis.txt")

# Nome do arquivo de entrada e saída
# json_file = "spiders/json_txt/urls.json"
# txt_file = "spiders/json_txt/links_imoveis.txt"

# txt_file
    # O arquivo já deve existir na pasta, criar um em branco caso nao tenha.
    # Os dados do links_imoveis.txt serão sobrescritos

# Abre e lê o arquivo JSON
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Coleta todos os links em uma lista
all_links = []
for item in data:
    all_links.extend(item["links"])  # Adiciona todos os links de cada página

# Salva os links no arquivo de texto, um por linha
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(all_links))

print(f"Arquivo '{input_path}' criado com {len(all_links)} links!")