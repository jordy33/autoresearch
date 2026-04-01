# proof-of-concept.md – Versión IA Automática (Demo Único con Parámetros Fijos)

**Objetivo del PoC**  
Demostrar que un script Python puede tomar un video de gameplay largo → detectar automáticamente un momento "épico" → generar un clip corto con voz IA hype, música y caption → listo para publicar.  
Todo con parámetros fijos (sin intervención manual en edición).  
Meta: 1 clip generado y publicado → rastrear vistas + primer $1 real vía afiliados.

**Requisitos previos (setup ~30-60 min, costo ~$0-5)**  
- Python 3.10+  
- FFmpeg instalado (global en PATH)  
- Librerías: `pip install faster-whisper elevenlabs pydub requests opencv-python yt-dlp`
- Cuenta ElevenLabs (plan Starter o free trial → clona voz de tu hijo con 1-2 min de audio hablando normal) → obtén API key  
- Cuenta TikTok + YouTube (puedes subir manual por ahora)  
- Opcional: código Creator de Epic Games (aplica en https://sac.epicgames.com – rápido si ya tienes links sociales)  

**Parámetros fijos del demo (hardcodeados en el script)**  
Estos son los que mencionaste — los ponemos como constantes para este PoC:

```python
# Config fija para PoC
HYPE_THRESHOLD = 0.75          # Umbral de "excitación" (normalizado 0-1) basado en volumen + detección de palabras clave
VOICE_STYLE = "voz de adolescente gamer mexicano emocionado, acento CDMX, hype total, energía alta, como si estuviera gritando una kill épica"
MUSIC_GENRE = "epic gaming trap"   # o "intense electronic" – busca en carpeta local o YouTube Audio Library
MUSIC_VOLUME = 0.25                # 25% del volumen principal para no tapar voz
HASHTAGS_TEMPLATE = "#Gaming #RobloxMexico #EpicMoment #FailOrWin #GamingClips #Shorts"
GAME_FOCUS = "Roblox"              # o "Fortnite" – enfocado en el juego que grabes
CLIP_DURATION = 30                 # segundos objetivo (15-45)
CAPTION_TEMPLATE = """🔥 {highlight_desc} en {game}! 😱 ¿Lo logré o fue fail total?  
Usa mi código Creator: {creator_code} y ayúdame a crecer 🔥  
{hashtags}"""
```

**Flujo del PoC (script demo.py)**
Crea un archivo demo.py con este esqueleto (lo completas con tus keys y paths). Este es el código base realista en 2026:

```python
import os
import subprocess
from faster_whisper import WhisperModel  # o usa whisper si prefieres CPU
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import cv2  # para extraer frames si quieres
import datetime

# ================== CONFIG ==================
INPUT_VIDEO = "raw/gameplay_roblox_2026-03-15.mp4"  # tu archivo grabado con OBS
OUTPUT_CLIP = "clips/demo_clip.mp4"
ELEVENLABS_API_KEY = "tu_key_aqui"
VOICE_ID = "tu_voice_id_clonada_de_tu_hijo"  # obtén después de clonar
CREATOR_CODE = "TU-CODIGO-EPIC"  # si ya tienes
# ============================================

model = WhisperModel("large-v3", device="cuda" if torch.cuda.is_available() else "cpu")
eleven = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def detect_hype_segments(audio_path, threshold=HYPE_THRESHOLD):
    # 1. Transcribe + timestamps con faster-whisper
    segments, info = model.transcribe(audio_path, language="es", vad_filter=True)
    
    hype_segments = []
    for seg in segments:
        text = seg.text.lower()
        # Detecta palabras clave de hype (gritos, emoción)
        hype_words = ["no mames", "qué", "wow", "epico", "kill", "vamos", "god", "insano", "!"]
        score = seg.avg_logprob  # proxy simple de energía + chequea volumen si extraes
        # Bonus: usa pydub para medir RMS en ese segmento y sumar score
        if any(w in text for w in hype_words) or score > -0.5:  # ajuste fino
            hype_segments.append((seg.start, seg.end, text))
    
    # Selecciona el segmento con mayor "hype" (el primero que supere threshold por ahora)
    if hype_segments:
        best = max(hype_segments, key=lambda x: x[1]-x[0])  # el más largo por simplicidad
        return best[0], best[1], best[2]
    return None, None, "Momento épico detectado!"

start, end, desc = detect_hype_segments(INPUT_VIDEO)  # asume extraes audio primero o usa video directo
if not start:
    print("No se detectó hype suficiente")
    exit()

# 2. Cortar clip con FFmpeg (15-45s centrado en hype)
duration = min(CLIP_DURATION, end - start + 10)  # padding
center = (start + end) / 2
cut_start = max(0, center - duration/2)
subprocess.run([
    "ffmpeg", "-i", INPUT_VIDEO, "-ss", str(cut_start), "-t", str(duration),
    "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264", "-preset", "fast", OUTPUT_CLIP, "-y"
])

# 3. Generar narración IA con ElevenLabs
prompt = f"¡{desc}! Esto fue totalmente insano en {GAME_FOCUS}. ¿Crees que lo logré?"
audio = eleven.text_to_speech.convert(
    text=prompt,
    voice_id=VOICE_ID,
    model_id="eleven_multilingual_v2",  # o turbo v2.5 si disponible
    output_format="mp3_44100_128"
)
with open("voiceover.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)

# 4. Mezclar voz + música + original audio bajo
voice = AudioSegment.from_mp3("voiceover.mp3") - 3  # bajar un poco
music = AudioSegment.from_file("music/epic_gaming.mp3") * MUSIC_VOLUME  # tu archivo local royalty-free
final_audio = voice.overlay(music)

# Exportar audio final
final_audio.export("final_audio.mp3", format="mp3")

# 5. Unir video + audio final con FFmpeg
subprocess.run([
    "ffmpeg", "-i", OUTPUT_CLIP, "-i", "final_audio.mp3",
    "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0",
    "final_demo.mp4", "-y"
])

# 6. Generar caption
hashtags = HASHTAGS_TEMPLATE
caption = CAPTION_TEMPLATE.format(
    highlight_desc=desc[:50],
    game=GAME_FOCUS,
    creator_code=CREATOR_CODE,
    hashtags=hashtags
)
print("\n=== CAPTION PARA COPIAR ===")
print(caption)
print("Sube final_demo.mp4 a TikTok / YouTube Shorts con esta caption")

print("PoC completado! Sube y rastrea vistas + clics en código Creator.")
```

**Pasos para ejecutar el PoC (1-2 horas total)**

1. Graba 20-40 min de gameplay (Roblox/Fortnite con reacciones en voz alta).
2. Coloca el `.mp4` en la carpeta y ajusta paths/keys.
3. Descarga 1 música royalty-free corta (~30s loop) y ponla en `music/`.
4. Corre `python demo.py` → genera `final_demo.mp4` + caption.
5. Sube manualmente a TikTok + YouTube Shorts.
6. Pon código Creator en bio y caption.
7. Espera 24-48h → revisa analytics + earnings en Epic dashboard.

**KPIs del PoC (mide manual o con sheet)**

- Clip generado OK? (sí/no)
- Duración correcta ~30s?
- Voz suena hype y natural?
- Vistas a 48h: >200 ideal
- Revenue: $0.01-$5 (cualquier compra vía tu código = validado)

Si funciona → validamos el core IA.
Próximo paso:

- Hacerlo batch (5 clips por video largo)
- Añadir TikTok Content Posting API (existe oficial en developers.tiktok.com → Content Posting API, soporta upload directo con OAuth, aprobación ~5-10 días)
- Integrar loop autoresearch (modificar parámetros según KPIs)
