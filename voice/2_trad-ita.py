from deep_translator import GoogleTranslator
from tqdm import tqdm  # Barra de progresso

with open("traduzir.srt", "r", encoding="utf-8") as f:
    linhas = f.readlines()

with open("traduzido_ita.srt", "w", encoding="utf-8") as f:
    for linha in tqdm(linhas, desc="Traduzindo"):
        if "-->" in linha or linha.strip().isdigit() or linha.strip() == "":
            f.write(linha)
        else:
            traducao = GoogleTranslator(source='pt', target='it).translate(linha.strip())
            f.write(traducao + "\n")
