import whisper
from moviepy.editor import VideoFileClip

# Caminhos dos arquivos
arquivo_video = "transcrever.mkv"
arquivo_audio = "audio_temp.wav"
arquivo_srt = "transcricao.srt"

# Função auxiliar para converter tempo em formato SRT
def formatar_tempo(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos_int = int(segundos % 60)
    milissegundos = int((segundos - int(segundos)) * 1000)
    return f"{horas:02}:{minutos:02}:{segundos_int:02},{milissegundos:03}"

# 1. Extrair áudio do vídeo
print("🎞️ Extraindo áudio do vídeo...")
clip = VideoFileClip(arquivo_video)
clip.audio.write_audiofile(arquivo_audio, codec='pcm_s16le')

# 2. Carregar modelo Whisper
print("🧠 Carregando modelo Whisper...")
modelo = whisper.load_model("base")  # Opções: tiny, base, small, medium, large

# 3. Transcrever áudio
print("📝 Transcrevendo áudio...")
resultado = modelo.transcribe(arquivo_audio, task="transcribe", language="pt")

# 4. Salvar legenda SRT
print("💾 Salvando transcrição em SRT...")
with open(arquivo_srt, "w", encoding="utf-8") as f:
    for i, segmento in enumerate(resultado["segments"], 1):
        f.write(f"{i}\n")
        f.write(f"{formatar_tempo(segmento['start'])} --> {formatar_tempo(segmento['end'])}\n")
        f.write(f"{segmento['text'].strip()}\n\n")

print(f"✅ Transcrição salva em: {arquivo_srt}")
