import asyncio
import edge_tts
from tqdm import tqdm

async def gerar_audio_com_progresso(texto, nome_arquivo, voz="pt-BR-AntonioNeural"):
    communicate = edge_tts.Communicate(texto, voice=voz)
    chunks = []
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            chunks.append(chunk["data"])

    # Barra de progresso
    with open(nome_arquivo, "wb") as f_out, tqdm(total=len(chunks), desc="Gerando áudio") as pbar:
        for chunk in chunks:
            f_out.write(chunk)
            pbar.update(1)

def main():
    with open("As Eras da Qualidade.txt", "r", encoding="utf-8") as f:
        texto = f.read()

    asyncio.run(gerar_audio_com_progresso(texto, "saida_audio.mp3"))

if __name__ == "__main__":
    main()
