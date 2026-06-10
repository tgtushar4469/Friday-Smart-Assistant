# ============================================================
#   FRIDAY AI v2.0 — brain.py
#   Groq (Llama 3.3 70B) powered intelligence
# ============================================================

import json, re
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, FRIDAY_SYSTEM_PROMPT, USER_NAME
from tools import TOOLS, run_tool

client       = None
history      = []
MAX_HISTORY  = 20


def _get_client():
    global client
    if client is None:
        client = Groq(api_key=GROQ_API_KEY)
    return client


# Quick mapping: keywords → tool names (for fast local detection)
KEYWORD_MAP = {
    # System
    "system info":["system_info"], "pc details":["system_info"], "pc info":["system_info"],
    "shutdown":["shutdown"], "band kar":["shutdown"], "restart":["restart"],
    "lock":["lock"], "screen lock":["lock"], "logout":["logout"],
    "sleep":["sleep"], "sone do":["sleep"],
    "game mode on":["game_mode_on"], "game mode off":["game_mode_off"],
    "task manager":["task_manager"], "update":["auto_update"],
    "virus scan":["virus_scan"], "antivirus":["virus_scan"],
    "temp clean":["clean_temp"], "junk":["clean_temp"], "clean karo":["clean_temp"],
    "recycle bin":["empty_trash"], "trash":["empty_trash"],
    "battery":["battery"], "charge":["battery"],
    "battery saver":["battery_saver"],
    "temperature":["cpu_temp"], "cpu temp":["cpu_temp"],
    "network speed":["network_speed"], "internet speed":["network_speed"],
    "wifi":["wifi_info"], "wi-fi":["wifi_info"],
    "bluetooth":["bluetooth"], "printer":["printer"],
    "phone link":["phone_link"],
    # Audio
    "mute mic":["mute_mic"], "unmute mic":["unmute_mic"],
    "mute":["mute"], "unmute":["unmute"],
    # Display
    "dark mode":["night_mode"], "night mode":["night_mode"],
    "light mode":["light_mode"], "day mode":["light_mode"],
    "eye care":["eye_care"], "night light":["eye_care"],
    "color picker":["color_picker"],
    # Screenshot
    "screenshot":["screenshot"], "snipping":["snipping_tool"],
    "screen record":["screen_record"], "record screen":["screen_record"],
    "stop record":["stop_record"],
    # Files
    "clipboard history":["clipboard_history"],
    "clipboard":["clipboard_get"],
    "downloads":["downloads"], "desktop":["desktop"],
    "hidden files":["show_hidden"],
    "refresh":["refresh_desktop"],
    "snap left":["snap_left"], "snap right":["snap_right"],
    # Time
    "time":["time"], "date":["time"], "kitna baja":["time"],
    # Productivity
    "stopwatch start":["stopwatch_start"], "stopwatch stop":["stopwatch_stop"],
    "pomodoro start":["pomodoro_start"], "pomodoro stop":["pomodoro_stop"],
    "todo":["todo"], "task list":["todo"],
    "excel":["excel_help"], "word help":["word_help"], "powerpoint":["ppt_help"],
    "invoice":["invoice"], "sign":["sign_doc"],
    "relax":["relax"], "calm":["relax"],
    "focus music":["focus_music"], "concentration":["focus_music"],
    # Web
    "news":["news"], "khabar":["news"],
    "meditation":["meditation"],
    "workout":["workout"], "exercise":["workout"],
    "diet":["diet"],
    "home decor":["home_decor"],
    "fashion":["fashion"],
    "food delivery":["food_delivery"], "swiggy":["food_delivery"], "zomato":["food_delivery"],
    "joke":["joke"], "jokes":["joke"], "funny":["joke"],
    "quote":["quote"], "motivat":["quote"],
    # Developer
    "docker":["docker"], "aws":["aws"], "deploy":["deploy"],
    "db tool":["db_tool"], "database":["db_tool"],
    "vscode":["vscode"], "vs code":["vscode"],
}


def _quick_detect(text: str):
    """Fast local keyword detection before calling Groq"""
    tl = text.lower()
    for kw, tools in KEYWORD_MAP.items():
        if kw in tl:
            return tools[0], {}
    return None, {}


def _groq_detect_tool(user_input: str) -> tuple:
    """Use Groq to detect tool + extract args"""
    tool_list = "\n".join(f"- {name}" for name in TOOLS.keys())

    prompt = f"""User said: "{user_input}"

Available tools:
{tool_list}

Extract the tool name and arguments from the user's message.
Respond ONLY with valid JSON, no markdown, no explanation:
{{"tool": "tool_name_or_none", "args": {{}}, "needs_tool": true_or_false}}

Examples:
"volume 60 karo" → {{"tool":"volume","args":{{"level":60}},"needs_tool":true}}
"chrome kholo" → {{"tool":"open_app","args":{{"app_name":"chrome"}},"needs_tool":true}}
"Mumbai ka weather" → {{"tool":"weather","args":{{"city":"Mumbai"}},"needs_tool":true}}
"50% brightness" → {{"tool":"brightness","args":{{"level":50}},"needs_tool":true}}
"alarm 7 30" → {{"tool":"alarm","args":{{"hour":7,"minute":30}},"needs_tool":true}}
"timer 5 minutes" → {{"tool":"timer","args":{{"minutes":5}},"needs_tool":true}}
"note: buy groceries" → {{"tool":"quick_note","args":{{"text":"buy groceries"}},"needs_tool":true}}
"search cats on youtube" → {{"tool":"youtube","args":{{"query":"cats"}},"needs_tool":true}}
"kya hal hai" → {{"tool":"none","args":{{}},"needs_tool":false}}
"mujhe ek joke sunao" → {{"tool":"joke","args":{{}},"needs_tool":true}}
"""
    try:
        r = _get_client().chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role":"user","content":prompt}],
            max_tokens=150, temperature=0.05)
        raw = r.choices[0].message.content.strip()
        raw = re.sub(r'```.*?```','', raw, flags=re.DOTALL).strip()
        data = json.loads(raw)
        tool = data.get("tool","none")
        args = data.get("args",{})
        needs = data.get("needs_tool", tool != "none")
        return (tool if needs and tool != "none" else None), args
    except Exception as e:
        print(f"[Tool Detect] {e}")
        return None, {}


def process_command(user_input: str) -> str:
    global history

    history.append({"role":"user","content":user_input})
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    # 1. Try fast local detect first
    tool_name, args = _quick_detect(user_input)

    # 2. If not found locally, ask Groq
    if not tool_name:
        tool_name, args = _groq_detect_tool(user_input)

    # 3. Run tool
    tool_result = None
    if tool_name and tool_name in TOOLS:
        tool_result = run_tool(tool_name, args)
        print(f"[Tool] {tool_name}({args}) → {tool_result}")

    # 4. Build final response with Groq
    sys_msgs = [{"role":"system","content":FRIDAY_SYSTEM_PROMPT}]
    chat_msgs = history[:-1]  # all except last

    if tool_result:
        cur = f'User: "{user_input}"\nTool ran: {tool_name}\nResult: {tool_result}\nConfirm briefly in a warm, natural way.'
    else:
        cur = user_input

    all_msgs = sys_msgs + chat_msgs + [{"role":"user","content":cur}]

    resp = _get_client().chat.completions.create(
        model=GROQ_MODEL, messages=all_msgs,
        max_tokens=250, temperature=0.82)

    reply = resp.choices[0].message.content.strip()
    history.append({"role":"assistant","content":reply})
    return reply


def clear_memory():
    global history
    history = []
    return "Memory clear kar di, fresh start!"


def get_greeting():
    import datetime
    h = datetime.datetime.now().hour
    if   5  <= h < 12: g = "Good morning"
    elif 12 <= h < 17: g = "Good afternoon"
    elif 17 <= h < 21: g = "Good evening"
    else:               g = "Working late again"
    from config import USER_NAME
    return f"{g}, {USER_NAME}! Friday online and fully operational. All systems ready, Boss. What do you need?"