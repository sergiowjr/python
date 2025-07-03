Atualize memória salva (elimina_tc-por_suite.py):

import requests
from requests.auth import HTTPBasicAuth

domain = "tfs.xpto.com"
collection = "Collection"
project = "Projeto"
plan_id = 12345
#suite_id = 112122
suite_id = input("Informe o ID da suite de testes: ")
pat = "zwr2...uklq"

auth = HTTPBasicAuth('', pat)
headers = {'Content-Type': 'application/json'}

url_list = f"https://{domain}/{collection}/{project}/_apis/test/Plans/{plan_id}/Suites/{suite_id}/TestCases?api-version=5.0"
print(f"URL para listar test cases: {url_list}")

response = requests.get(url_list, auth=auth, headers=headers)

if response.status_code != 200:
    print(f"Erro {response.status_code}: {response.text}")
    exit()

cases = response.json().get("value", [])
num_cases = len(cases)
print(f"Encontrados {num_cases} casos.")

if num_cases == 0:
    print("Nada para deletar. Encerrando.")
    exit()

confirm = input("Deseja realmente excluir esses test cases? Digite 'sim' para confirmar: ").strip().lower()
if confirm != 'sim':
    print("Operação abortada pelo usuário.")
    exit()

for case in cases:
    case_id = case["testCase"]["id"]
    url_delete = f"https://{domain}/{collection}/{project}/_apis/test/testcases/{case_id}?api-version=5.0"
    del_resp = requests.delete(url_delete, auth=auth, headers=headers)
    if del_resp.status_code == 204:
        print(f"Deletado TC {case_id} com sucesso")
    else:
        print(f"Erro ao deletar TC {case_id}: {del_resp.status_code} - {del_resp.text}")
