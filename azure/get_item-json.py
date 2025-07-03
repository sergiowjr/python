import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import json

# Parâmetros de entrada
domain = "tfs.xpto.com"
azure_organization = "Collection"  # Substitua se necessário
azure_project = "Project"          # Substitua se necessário
work_item_id = 123456              # Substitua pelo ID real
pat = "zwr2...uklq"                # Seu Personal Access Token do Azure DevOps

# Montar URL do endpoint
#url = f"https://{domain}/{azure_organization}/{azure_project}/_apis/wit/workitems/{work_item_id}?api-version=7.1-preview.3"
url = f"https://{domain}/{azure_organization}/{azure_project}/_apis/wit/workitems/{work_item_id}?api-version=7.1-preview.3&$expand=all"

# === Autenticação e headers ===
auth = HTTPBasicAuth('', pat)
headers = {'Content-Type': 'application/json'}

# === Executa requisição ===
response = requests.get(url, auth=auth, headers=headers)

# === Trata resposta ===
if response.status_code == 200:
    dados = response.json()

    # Gera timestamp no formato YYYYMMDDHHMM
    timestamp = datetime.now().strftime("%Y%m%d%H%M")

    # Monta nome do arquivo
    nome_arquivo = f"{work_item_id}_{timestamp}.json"

    # Salva o conteúdo no arquivo
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print(f"✅ Arquivo salvo como: {nome_arquivo}")
else:
    print(f"❌ Erro ao consultar Work Item: {response.status_code}")
    print(response.text)
