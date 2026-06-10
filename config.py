# ============================================================
#   FRIDAY AI v2.0 — config.py
#   ⚠️  SIRF YAHAN APNI KEYS DAALO — BAAKI KUCH MAT CHHUO!
# ============================================================

# ── STEP 1: Groq API Key ─────────────────────────────────────
# Free key lo: https://console.groq.com → API Keys → Create
GROQ_API_KEY = "YAHAN_APNI_GROQ_KEY_DAALO"

# ── STEP 2: ElevenLabs API Key (Beautiful Girl Voice) ────────
# Free key lo: https://elevenlabs.io → Profile → API Key
ELEVENLABS_API_KEY = "YAHAN_APNI_ELEVENLABS_KEY_DAALO"

# ── STEP 3: SerpAPI (Web Search) — Optional ──────────────────
# Free key lo: https://serpapi.com
SERPAPI_KEY = "YAHAN_APNI_SERPAPI_KEY_DAALO"

# ── STEP 4: OpenWeather (Weather) — Optional ─────────────────
# Free key lo: https://openweathermap.org/api
OPENWEATHER_KEY = "YAHAN_APNI_WEATHER_KEY_DAALO"

# =============================================================
#   PERSONAL SETTINGS — Apna naam etc.
# =============================================================
USER_NAME        = "Tushar"
ASSISTANT_NAME   = "Friday"
WAKE_WORD        = "hello friday"
GROQ_MODEL       = "llama-3.3-70b-versatile"

# ElevenLabs Voice IDs (beautiful girl voices — free tier)
# Rachel  = "21m00Tcm4TlvDq8ikWAM"  ← Default (recommended)
# Bella   = "EXAVITQu4vr4xnSDxMaL"
# Domi    = "AZnzlk1XvdvUeBnXmlld"
# Elli    = "MF3mGyEYCl7XYWbV9V6O"
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

USE_OFFLINE_VOICE_BACKUP = True   # ElevenLabs fail ho to Windows voice use karo
SPEAK_RESPONSES          = True   # Friday bolegi ya sirf text dikhayegi

# Friday ka personality
FRIDAY_SYSTEM_PROMPT = f"""You are FRIDAY — an advanced, witty, warm AI personal assistant for {USER_NAME} (your boss).
Personality: Like Iron Man's FRIDAY — confident, intelligent, slightly playful, always helpful.
Voice: Beautiful, calm, professional female tone.

RULES:
- Call user "{USER_NAME}" or "Boss"
- Keep replies SHORT (2-3 sentences) unless detail is needed
- When a tool runs, confirm briefly: "Done Boss! Volume set to 50%."
- Understand BOTH English AND Hindi/Hinglish — reply in whatever language the user uses
- Never say you are OpenAI/Google/Anthropic — you are FRIDAY, built for {USER_NAME}
- Be proactive, suggest things when useful
- Add small personality touches — occasional wit, warmth
- You run 24/7 on {USER_NAME}'s Windows 11 laptop with full system access
"""