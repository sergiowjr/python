import asyncio
import pysrt
import os
from pydub import AudioSegment
from tqdm import tqdm
import edge_tts

# Parâmetros
arquivo_srt = "traduzido_eng.srt"
voz = "en-US-GuyNeural"  # Outras opções: en-US-JennyNeural, en-US-AriaNeural
pasta_temp = "audios_temp"
arquivo_saida = "output_final_en.mp3"

# Cria pasta temporária se não existir
os.makedirs(pasta_temp, exist_ok=True)

# Lê legendas
legendas = pysrt.open(arquivo_srt)
duracao_total = legendas[-1].end.ordinal + 1000  # margem extra de 1s
faixa_final = AudioSegment.silent(duration=duracao_total)

# Função assíncrona para gerar áudio com edge-tts
async def gerar_audio(texto, caminho_saida):
    communicate = edge_tts.Communicate(texto, voice=voz, rate="-17%")
    await communicate.save(caminho_saida)

# Processar cada legenda
print("Generating English voiceovers...")
for legenda in tqdm(legendas):
    texto = legenda.text.strip().replace('\n', ' ')
    nome_arquivo = os.path.join(pasta_temp, f"{legenda.index}.mp3")
    
    # Gerar áudio
    asyncio.run(gerar_audio(texto, nome_arquivo))

    # Carregar áudio e ajustar posição
    audio = AudioSegment.from_file(nome_arquivo)
    tempo_legenda = legenda.end.ordinal - legenda.start.ordinal
    dur_audio = len(audio)

    if dur_audio < tempo_legenda:
        pausa = AudioSegment.silent(duration=(tempo_legenda - dur_audio))
        audio += pausa

    faixa_final = faixa_final.overlay(audio, position=legenda.start.ordinal)

# Exportar áudio final
faixa_final.export(arquivo_saida, format="mp3")
print(f"\n✅ English dubbing generated: {arquivo_saida}")
