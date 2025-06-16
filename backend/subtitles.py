import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY", "")

audio_file = "outputs/output.mp3"

config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)

transcript = aai.Transcriber(config=config).transcribe(audio_file)

if transcript.status == "error":
    raise RuntimeError(f"Transcription failed: {transcript.error}")

# Save transcript text to outputs/subtitles.txt
with open("outputs/subtitles.txt", "w", encoding="utf-8") as f:
    f.write(transcript.text)
print("✅ Subtitles saved as outputs/subtitles.txt")