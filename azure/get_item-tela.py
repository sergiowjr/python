import requests
from requests.auth import HTTPBasicAuth

# Parâmetros de entrada
domain = "tfs.xpto.com"
azure_organization = "Collection"  # Exemplo
azure_project = "Projeto"          # Exemplo
work_item_id = 123456              # Substitua pelo ID real
pat = "zwr2...uklq"                # Seu Personal Access Token do Azure DevOps

# Montar URL do endpoint
#url = f"https://{domain}/{azure_organization}/{azure_project}/_apis/wit/workitems/{work_item_id}?api-version=7.1-preview.3"
url = f"https://{domain}/{azure_organization}/{azure_project}/_apis/wit/workitems/{work_item_id}?api-version=7.1-preview.3&$expand=all"

# Requisição com autenticação básica (usuário em branco, PAT como senha)
response = requests.get(url, auth=HTTPBasicAuth('', pat))

# Verificar resposta
if response.status_code == 200:
    dados = response.json()
    print("=== Campos do Work Item ===")
    for campo, valor in dados.get("fields", {}).items():
        print(f"{campo}: {valor}")
else:
    print(f"Erro ao consultar Work Item: {response.status_code}")
    print(response.text)
