# ============================================================
#   FRIDAY AI v2.0 — wake_word.py
#   "Hello Friday" detection + speech recognition
# ============================================================

import speech_recognition as sr
import threading
from config import WAKE_WORD

_recognizer = sr.Recognizer()
_recognizer.energy_threshold    = 2500
_recognizer.dynamic_energy_threshold = True
_listening   = True
_callback    = None


def start_wake_detection(callback):
    global _callback
    _callback = callback
    t = threading.Thread(target=_wake_loop, daemon=True)
    t.start()
    return t


def _wake_loop():
    global _listening
    print(f"[FRIDAY] Wake word active → say '{WAKE_WORD}'")
    with sr.Microphone() as src:
        _recognizer.adjust_for_ambient_noise(src, duration=1)
        while _listening:
            try:
                audio = _recognizer.listen(src, timeout=1, phrase_time_limit=4)
                text  = _recognizer.recognize_google(audio).lower()
                if WAKE_WORD.lower() in text:
                    print(f"[Wake] '{text}' → triggered!")
                    if _callback: _callback()
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception:
                pass


def listen_once(timeout: int = 10) -> str:
    with sr.Microphone() as src:
        _recognizer.adjust_for_ambient_noise(src, duration=0.3)
        print("[FRIDAY] Listening...")
        try:
            audio = _recognizer.listen(src, timeout=timeout, phrase_time_limit=20)
            text  = _recognizer.recognize_google(audio)
            print(f"[You] {text}")
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"[Listen Error] {e}")
            return ""


def stop():
    global _listening
    _listening = False