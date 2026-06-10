# ============================================================
#   FRIDAY AI v2.0 — voice.py
#   ElevenLabs beautiful girl voice + offline backup
# ============================================================

import os, threading, tempfile, requests
import pyttsx3, pygame
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, SPEAK_RESPONSES

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

_offline_engine = None

def _get_offline_engine():
    global _offline_engine
    if _offline_engine is None:
        _offline_engine = pyttsx3.init()
        voices = _offline_engine.getProperty('voices')
        # Female voice prefer karo
        for v in voices:
            if any(x in v.name.lower() for x in ['female','zira','hazel','susan','catherine']):
                _offline_engine.setProperty('voice', v.id)
                break
        _offline_engine.setProperty('rate',   178)
        _offline_engine.setProperty('volume', 1.0)
    return _offline_engine

def speak(text: str, use_online: bool = True):
    if not SPEAK_RESPONSES:
        print(f"\n🤖 FRIDAY: {text}\n")
        return
    print(f"\n🤖 FRIDAY: {text}\n")
    if use_online and ELEVENLABS_API_KEY not in ("YAHAN_APNI_ELEVENLABS_KEY_DAALO",""):
        if _speak_elevenlabs(text):
            return
    _speak_offline(text)

def _speak_elevenlabs(text: str) -> bool:
    try:
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
            headers={"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"},
            json={"text": text[:500],
                  "model_id": "eleven_monolingual_v1",
                  "voice_settings": {"stability":0.5,"similarity_boost":0.8,"style":0.2}},
            timeout=10)
        if r.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(r.content); tmp = f.name
            pygame.mixer.music.load(tmp)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.unlink(tmp)
            return True
    except Exception as e:
        print(f"[ElevenLabs] {e}")
    return False

def _speak_offline(text: str):
    try:
        e = _get_offline_engine()
        e.say(text); e.runAndWait()
    except Exception as e:
        print(f"[Offline TTS] {e}")

def speak_async(text: str):
    threading.Thread(target=speak, args=(text,), daemon=True).start()