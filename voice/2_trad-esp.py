from deep_translator import GoogleTranslator

with open("traduzir.srt", "r", encoding="utf-8") as f:
    linhas = f.readlines()

with open("traduzido_esp.srt", "w", encoding="utf-8") as f:
    for linha in linhas:
        if "-->" in linha or linha.strip().isdigit() or linha.strip() == "":
            f.write(linha)
        else:
            traducao = GoogleTranslator(source='pt', target='es').translate(linha.strip())
            f.write(traducao + "\n")
