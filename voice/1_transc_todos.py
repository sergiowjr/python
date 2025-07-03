import os
import whisper

# Caminho da pasta onde estão os arquivos .wav
pasta_wav = r'C:\Users\Jr\Documents\Gravações de som'

# Modelo de transcrição (pode ser 'tiny', 'base', 'small', 'medium', 'large')
modelo = whisper.load_model('large')

# Percorrer todos os arquivos .wav na pasta
for arquivo in os.listdir(pasta_wav):
    if arquivo.endswith('.wav'):
        caminho_arquivo = os.path.join(pasta_wav, arquivo)
        print(f"Transcrevendo: {arquivo}")

        # Transcrever o áudio
        resultado = modelo.transcribe(caminho_arquivo)

        # Nome do arquivo de saída .txt
        arquivo_saida = os.path.join(pasta_wav, f"{os.path.splitext(arquivo)[0]}.txt")

        # Salvar a transcrição
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(resultado['text'])

print("✅ Transcrição finalizada para todos os arquivos.")
