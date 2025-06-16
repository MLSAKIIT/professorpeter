import json
from elevenlabs.client import ElevenLabs
import os

# Load script from topic.json
with open("outputs/topic.json", "r", encoding="utf-8") as f:
    script_data = json.load(f)

# Extract the narration text (concatenate all audio_script segments)
if "audio_script" in script_data:
    text = " ".join([seg["text"] for seg in script_data["audio_script"] if "text" in seg])
else:
    # fallback: try to use overall_narrative or key_sections
    text = script_data.get("overall_narrative", "")
    if not text and "key_sections" in script_data:
        text = " ".join([section.get("narration_text", "") for section in script_data["key_sections"]])

# Replace with your actual API key
client = ElevenLabs(api_key="sk_1a71d32f20d030ebd5ff529b678604c0aaf0a24e03b990ce")

# Generate audio using your custom voice
audio = client.text_to_speech.convert(
    voice_id="NNWUYwHysl0Zcr6gTZy4",       # Your voice ID
    text=text,
    output_format="mp3_44100_128",        # High quality MP3
    model_id="eleven_multilingual_v2",   # Recommended model
    voice_settings={
        "stability": 0.6,
        "similarity_boost": 0.8
    }
)

# Save the result to a file in outputs directory
os.makedirs("outputs", exist_ok=True)
with open("outputs/output.mp3", "wb") as f:
    f.write(b"".join(audio))
print("✅ Audio saved as outputs/output.mp3")
