import requests
from requests.auth import HTTPBasicAuth
import sys
import os
from datetime import datetime

# === Configuração ===
domain = "tfs.xpto.com"
collection = "PrintCollection"
project = "Project"
plan_id = 123456

# === Entrada do usuário ===
suite_id = input("Informe o ID da suite de testes: ").strip()
if not suite_id.isdigit():
    print("❌ ID da suite inválido. Deve ser numérico.")
    sys.exit(1)

# === Autenticação ===
# Por segurança, prefira usar variável de ambiente ao invés de hardcoded
pat = os.getenv("AZURE_PAT") or "zwr2...uklq"
auth = HTTPBasicAuth('', pat)
headers = {'Content-Type': 'application/json'}

# === Monta URL para listar Test Cases ===
url_list = f"https://{domain}/{collection}/{project}/_apis/test/Plans/{plan_id}/Suites/{suite_id}/TestCases?api-version=5.0"
print(f"🔍 Consultando test cases da suite {suite_id}...")

try:
    response = requests.get(url_list, auth=auth, headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"❌ Erro ao consultar test cases: {e}")
    sys.exit(1)

cases = response.json().get("value", [])
num_cases = len(cases)
print(f"📋 Encontrados {num_cases} casos.")

if num_cases == 0:
    print("⚠️ Nada para deletar. Encerrando.")
    sys.exit(0)

confirm = input("❗ Deseja realmente excluir esses test cases? Digite 'sim' para confirmar: ").strip().lower()
if confirm != 'sim':
    print("🚫 Operação abortada pelo usuário.")
    sys.exit(0)

# === Log de exclusão ===
timestamp = datetime.now().strftime("%Y%m%d%H%M")
log_filename = f"delecao_suite_{suite_id}_{timestamp}.log"
sucesso, falha = 0, 0

with open(log_filename, "w", encoding="utf-8") as log:
    log.write(f"Log de exclusão - suite {suite_id} - {timestamp}\n\n")

    for case in cases:
        case_id = case["testCase"]["id"]
        url_delete = f"https://{domain}/{collection}/{project}/_apis/test/testcases/{case_id}?api-version=5.0"
        try:
            del_resp = requests.delete(url_delete, auth=auth, headers=headers)
            if del_resp.status_code == 204:
                print(f"✅ Deletado TC {case_id} com sucesso")
                log.write(f"OK  - TC {case_id} deletado com sucesso\n")
                sucesso += 1
            else:
                print(f"❌ Erro ao deletar TC {case_id}: {del_resp.status_code}")
                log.write(f"ERRO - TC {case_id}: {del_resp.status_code} - {del_resp.text}\n")
                falha += 1
        except requests.exceptions.RequestException as e:
            print(f"❌ Falha na exclusão do TC {case_id}: {e}")
            log.write(f"EXCEÇÃO - TC {case_id}: {e}\n")
            falha += 1

print(f"\n🧾 Resumo:")
print(f"✔️  Sucesso: {sucesso}")
print(f"❌  Falhas: {falha}")
print(f"📁 Log salvo em: {log_filename}")
