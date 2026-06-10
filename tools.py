# ============================================================
#   FRIDAY AI v2.0 — tools.py
#   ALL 100+ capabilities in one file
# ============================================================

import os, sys, subprocess, platform, shutil, webbrowser
import ctypes, winreg, zipfile, time, datetime, threading
import psutil, pyperclip, glob, json, re, tempfile, socket
from pathlib import Path

# ============================================================
#  1. SYSTEM INFO & CONTROL
# ============================================================

def get_system_info():
    cpu = platform.processor()
    ram_total = round(psutil.virtual_memory().total / (1024**3), 1)
    ram_used  = psutil.virtual_memory().percent
    disk      = psutil.disk_usage('C:\\')
    disk_total= round(disk.total / (1024**3), 1)
    disk_used = round(disk.used  / (1024**3), 1)
    return (f"OS: {platform.system()} {platform.release()} | PC: {platform.node()}\n"
            f"CPU: {cpu[:50]}\nRAM: {ram_used}% used of {ram_total}GB\n"
            f"Disk C: {disk_used}GB used of {disk_total}GB")

def shutdown_pc():
    os.system("shutdown /s /t 5"); return "PC 5 sec mein shutdown, Boss!"

def restart_pc():
    os.system("shutdown /r /t 5"); return "PC 5 sec mein restart, Boss!"

def lock_screen():
    ctypes.windll.user32.LockWorkStation(); return "Screen lock kar di, Boss!"

def logout_user():
    os.system("shutdown /l"); return "Logging out..."

def sleep_pc():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return "PC sleep mode mein ja raha hai, Boss!"

def sync_time():
    subprocess.run("w32tm /resync", shell=True, capture_output=True)
    return "System time sync kar diya, Boss!"

def enable_game_mode():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\GameBar", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AutoGameModeEnabled", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        subprocess.Popen("GameBarFTServer", shell=True)
    except: pass
    return "Game Mode ON! Performance boost kar diya, Boss! 🎮"

def disable_game_mode():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\GameBar", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AutoGameModeEnabled", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    except: pass
    return "Game Mode OFF kar diya!"

def open_task_manager():
    subprocess.Popen("taskmgr", shell=True); return "Task Manager khol diya!"

def auto_update():
    subprocess.Popen("wuauclt /detectnow /updatenow", shell=True)
    return "Windows Update check shuru kar diya, Boss!"

def open_phone_link():
    subprocess.Popen("start ms-phone:", shell=True)
    return "Phone Link app khol raha hoon!"

# ============================================================
#  2. VOLUME & AUDIO
# ============================================================

def set_volume(level: int):
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        vol = cast(interface, POINTER(IAudioEndpointVolume))
        vol.SetMasterVolumeLevelScalar(max(0.0, min(1.0, level/100)), None)
        return f"Volume {level}% kar diya, Boss!"
    except:
        # Fallback: nircmd
        subprocess.run(f"nircmd setsysvolume {int(level*655.35)}", shell=True)
        return f"Volume {level}% set kar diya!"

def mute_volume():
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        vol = cast(interface, POINTER(IAudioEndpointVolume))
        vol.SetMute(1, None)
    except:
        subprocess.run("nircmd mutesysvolume 1", shell=True)
    return "Mute kar diya, Boss!"

def unmute_volume():
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        vol = cast(interface, POINTER(IAudioEndpointVolume))
        vol.SetMute(0, None)
    except:
        subprocess.run("nircmd mutesysvolume 0", shell=True)
    return "Unmute kar diya, Boss!"

def mute_mic():
    subprocess.run('powershell -c "Set-AudioDevice -RecordingMute $True"', shell=True)
    return "Microphone mute kar diya!"

def unmute_mic():
    subprocess.run('powershell -c "Set-AudioDevice -RecordingMute $False"', shell=True)
    return "Microphone unmute kar diya!"

# ============================================================
#  3. DISPLAY
# ============================================================

def set_brightness(level: int):
    try:
        import screen_brightness_control as sbc
        sbc.set_brightness(level)
        return f"Brightness {level}% kar diya, Boss!"
    except:
        subprocess.run(
            f'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"',
            shell=True)
        return f"Brightness {level}% set kiya!"

def enable_night_mode():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AppsUseLightTheme",   0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(key, "SystemUsesLightTheme",0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    except: pass
    return "Dark mode ON kar diya, Boss! 🌙"

def enable_light_mode():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AppsUseLightTheme",   0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "SystemUsesLightTheme",0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except: pass
    return "Light mode ON kar diya!"

def enable_eye_care():
    """Blue light filter / Night light on"""
    subprocess.Popen("start ms-settings:nightlight", shell=True)
    return "Eye Care (Night Light) settings khol di, Boss! Wahan ON karo."

def open_color_picker():
    subprocess.Popen("powertoys", shell=True)
    return "PowerToys Color Picker khol raha hoon! (Win + Shift + C)"

# ============================================================
#  4. SCREENSHOT & SCREEN RECORDING
# ============================================================

def take_screenshot(region=None):
    try:
        import pyautogui
        ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(os.path.expanduser("~"), "Pictures", f"Friday_{ts}.png")
        img  = pyautogui.screenshot()
        img.save(path)
        os.startfile(path)
        return f"Screenshot liya aur khol diya: {path}"
    except Exception as e:
        return f"Screenshot error: {e}"

def open_snipping_tool():
    subprocess.Popen("SnippingTool.exe", shell=True)
    return "Snipping Tool khol diya! (Win+Shift+S se bhi kaam karta hai)"

def start_screen_recording():
    """Windows built-in Xbox Game Bar recording"""
    import pyautogui
    pyautogui.hotkey('win', 'alt', 'r')
    return "Screen recording shuru! (Win+Alt+R se band karo)"

def stop_screen_recording():
    import pyautogui
    pyautogui.hotkey('win', 'alt', 'r')
    return "Screen recording band kar di, Boss!"

# ============================================================
#  5. BATTERY & PERFORMANCE
# ============================================================

def get_battery_info():
    b = psutil.sensors_battery()
    if b:
        status = "Charging ⚡" if b.power_plugged else "Discharging 🔋"
        mins   = int(b.secsleft / 60) if b.secsleft > 0 and not b.power_plugged else 0
        time_left = f" — ~{mins} min remaining" if mins > 0 else ""
        return f"Battery: {b.percent:.0f}% | {status}{time_left}"
    return "Battery info nahi mili (desktop PC?)"

def enable_battery_saver():
    subprocess.run(
        'powershell -c "powercfg /setactive 77077ee2-1188-4e9b-b196-57aa1406d46e"',
        shell=True)
    return "Battery Saver mode ON kar diya, Boss! 🔋"

def get_cpu_temp():
    try:
        result = subprocess.run(
            'powershell -c "Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace root/wmi | Select CurrentTemperature"',
            capture_output=True, text=True, shell=True)
        lines = [l for l in result.stdout.splitlines() if l.strip().isdigit()]
        if lines:
            temp_k = int(lines[0].strip())
            temp_c = (temp_k - 2732) / 10.0
            return f"CPU Temperature: {temp_c:.1f}°C"
    except: pass
    return "Temperature sensor direct access nahi mila. HWMonitor install karo."

def check_network_speed():
    """Simple speed estimate via socket"""
    try:
        import urllib.request, time as t
        start = t.time()
        urllib.request.urlretrieve("http://speedtest.tele2.net/1MB.zip", os.devnull)
        elapsed = t.time() - start
        speed_mbps = round((1 * 8) / elapsed, 2)
        return f"Approximate Download Speed: ~{speed_mbps} Mbps"
    except:
        webbrowser.open("https://fast.com")
        return "Speed test browser mein khol diya (fast.com)"

def get_wifi_info():
    result = subprocess.run("netsh wlan show interfaces", capture_output=True, text=True, shell=True)
    lines  = result.stdout.splitlines()
    info   = {}
    for line in lines:
        if "SSID" in line and "BSSID" not in line:
            info["WiFi"] = line.split(":")[1].strip()
        if "Signal" in line:
            info["Signal"] = line.split(":")[1].strip()
        if "Receive rate" in line:
            info["Speed"] = line.split(":")[1].strip()
    if info:
        return " | ".join(f"{k}: {v}" for k, v in info.items())
    return "WiFi info nahi mili ya connected nahi ho."

def open_wifi_settings():
    subprocess.Popen("start ms-settings:network-wifi", shell=True)
    return "WiFi settings khol di, Boss!"

def open_bluetooth_settings():
    subprocess.Popen("start ms-settings:bluetooth", shell=True)
    return "Bluetooth settings khol di!"

def open_printer_settings():
    subprocess.Popen("start ms-settings:printers", shell=True)
    return "Printer settings khol di!"

def virus_scan():
    subprocess.Popen(
        r'"C:\Program Files\Windows Defender\MpCmdRun.exe" -Scan -ScanType 1',
        shell=True)
    return "Windows Defender quick scan shuru kar diya, Boss!"

def clean_temp_files():
    cleaned = 0
    temp_dirs = [os.environ.get('TEMP',''), os.environ.get('TMP',''),
                 os.path.join(os.environ.get('LOCALAPPDATA',''), 'Temp')]
    for d in set(temp_dirs):
        if d and os.path.exists(d):
            for item in os.listdir(d):
                try:
                    p = os.path.join(d, item)
                    if os.path.isfile(p): os.remove(p)
                    else: shutil.rmtree(p)
                    cleaned += 1
                except: pass
    # Also run disk cleanup
    subprocess.Popen("cleanmgr /sagerun:1", shell=True)
    return f"Temp files clean kar diye! ({cleaned} items), Disk Cleanup bhi shuru kiya."

def empty_recycle_bin():
    try:
        import winshell
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        return "Recycle Bin khali kar di, Boss!"
    except:
        subprocess.run(
            'powershell -c "Clear-RecycleBin -Force"', shell=True)
        return "Recycle Bin khali kar di!"

# ============================================================
#  6. MOUSE & KEYBOARD
# ============================================================

def set_mouse_speed(speed: int):
    """Speed 1-20"""
    try:
        SPI_SETMOUSESPEED = 0x0071
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETMOUSESPEED, 0, speed, 3)
        return f"Mouse speed {speed} kar diya, Boss!"
    except Exception as e:
        return f"Mouse speed error: {e}"

def set_keyboard_backlight(level: int = 1):
    """Many laptops support this via WMI"""
    return "Keyboard backlight: Tumhare laptop ke manufacturer software se control hoga (Asus Armory, Lenovo Vantage, etc.)"

# ============================================================
#  7. APPS & FILES
# ============================================================

APP_MAP = {
    "chrome": "chrome", "firefox": "firefox", "edge": "msedge",
    "notepad": "notepad", "calculator": "calc", "paint": "mspaint",
    "word": "winword", "excel": "excel", "powerpoint": "powerpnt",
    "vscode": "code", "vs code": "code",
    "task manager": "taskmgr", "taskmgr": "taskmgr",
    "control panel": "control", "settings": "ms-settings:",
    "file explorer": "explorer", "explorer": "explorer",
    "cmd": "cmd", "command prompt": "cmd",
    "powershell": "powershell",
    "vlc": "vlc", "spotify": "spotify", "discord": "discord",
    "whatsapp": "whatsapp", "telegram": "telegram",
    "zoom": "zoom", "teams": "teams", "slack": "slack",
    "outlook": "outlook", "mail": "ms-email:",
    "camera": "microsoft.windows.camera:",
    "photos": "ms-photos:", "store": "ms-windows-store:",
    "paint 3d": "ms-paint:",
    "snipping tool": "SnippingTool.exe",
    "notepad++": "notepad++",
    "obs": "obs64", "obs studio": "obs64",
}

def open_app(app_name: str):
    key = app_name.lower().strip()
    cmd = APP_MAP.get(key, app_name)
    try:
        if cmd.startswith("ms-") or cmd.startswith("microsoft"):
            subprocess.Popen(f"start {cmd}", shell=True)
        else:
            subprocess.Popen(cmd, shell=True)
        return f"{app_name} khol diya, Boss!"
    except Exception as e:
        return f"'{app_name}' nahi mila. Check karo installed hai ya nahi."

def open_file(path: str):
    path = path.strip('"')
    if os.path.exists(path):
        os.startfile(path); return f"Khol diya: {path}"
    return f"File nahi mili: {path}"

def search_file(name: str, root: str = None):
    if root is None:
        root = os.path.expanduser("~")
    results = []
    try:
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in
                       ['Windows','System32','$Recycle.Bin','AppData','node_modules','.git']]
            for f in files:
                if name.lower() in f.lower():
                    results.append(os.path.join(dirpath, f))
                if len(results) >= 8: break
            if len(results) >= 8: break
    except: pass
    if results: return "Mili files:\n" + "\n".join(results)
    return f"'{name}' nahi mili."

def create_folder(path: str):
    os.makedirs(path, exist_ok=True); return f"Folder bana diya: {path}"

def delete_file(path: str):
    path = path.strip('"')
    if not os.path.exists(path): return f"Nahi mila: {path}"
    if os.path.isfile(path): os.remove(path)
    else: shutil.rmtree(path)
    return f"Delete kar diya: {path}"

def rename_file(old_path: str, new_name: str):
    dir_ = os.path.dirname(old_path)
    new_path = os.path.join(dir_, new_name)
    os.rename(old_path, new_path)
    return f"Rename kar diya: {new_name}"

def shred_file(path: str):
    """Secure delete — overwrite then delete"""
    path = path.strip('"')
    if not os.path.exists(path): return "File nahi mili."
    with open(path, 'ba+') as f:
        length = f.seek(0, 2)
        for _ in range(3):
            f.seek(0); f.write(os.urandom(length))
    os.remove(path)
    return f"File permanently shred kar di (3-pass overwrite): {path}"

def zip_files(files_str: str, output: str):
    files = [f.strip() for f in files_str.split(",")]
    with zipfile.ZipFile(output,'w', zipfile.ZIP_DEFLATED) as z:
        for f in files:
            if os.path.exists(f): z.write(f, os.path.basename(f))
    return f"ZIP bana diya: {output}"

def unzip_file(zip_path: str, extract_to: str = None):
    zip_path = zip_path.strip('"')
    if extract_to is None:
        extract_to = os.path.dirname(zip_path)
    with zipfile.ZipFile(zip_path,'r') as z: z.extractall(extract_to)
    return f"Extract kar diya: {extract_to}"

def hide_file(path: str):
    subprocess.run(f'attrib +h "{path}"', shell=True)
    return f"File hide kar di: {path}"

def show_hidden_files():
    subprocess.run(
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v Hidden /t REG_DWORD /d 1 /f',
        shell=True)
    subprocess.run('taskkill /f /im explorer.exe && start explorer.exe', shell=True)
    return "Hidden files visible kar diye, Boss!"

def copy_path(path: str):
    pyperclip.copy(path)
    return f"Path clipboard mein copy kar diya: {path}"

def get_folder_size(path: str):
    total = sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, _, fnames in os.walk(path)
        for f in fnames
        if os.path.exists(os.path.join(dp, f))
    )
    gb = round(total/1024**3, 2); mb = round(total/1024**2, 1)
    return f"{path}: {gb}GB ({mb}MB)"

def make_shortcut(target: str, shortcut_path: str = None):
    try:
        import win32com.client
        if shortcut_path is None:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            name    = os.path.splitext(os.path.basename(target))[0]
            shortcut_path = os.path.join(desktop, f"{name}.lnk")
        shell = win32com.client.Dispatch("WScript.Shell")
        sc    = shell.CreateShortCut(shortcut_path)
        sc.Targetpath = target
        sc.save()
        return f"Shortcut bana diya Desktop pe: {shortcut_path}"
    except Exception as e:
        return f"Shortcut error: {e}"

def change_wallpaper(path: str):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path.strip('"'), 3)
    return f"Wallpaper change kar diya, Boss!"

def hide_desktop_icons():
    import pyautogui
    pyautogui.hotkey('win', 'd')
    return "Desktop show/hide kar diya!"

def refresh_desktop():
    import pyautogui
    pyautogui.hotkey('f5')
    return "Desktop refresh kar diya!"

def snap_window_left():
    import pyautogui
    pyautogui.hotkey('win', 'left')
    return "Window left snap kar diya!"

def snap_window_right():
    import pyautogui
    pyautogui.hotkey('win', 'right')
    return "Window right snap kar diya!"

def pin_window_on_top():
    return "Pin on top ke liye: PowerToys install karo → Always on Top (Win+Ctrl+T)"

def open_clipboard_history():
    import pyautogui
    pyautogui.hotkey('win', 'v')
    return "Clipboard History khol diya! (Win+V)"

def get_clipboard():
    return pyperclip.paste() or "Clipboard empty hai."

def set_clipboard(text: str):
    pyperclip.copy(text); return "Clipboard mein copy kar diya!"

def open_downloads():
    path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.startfile(path); return "Downloads folder khol diya!"

def open_desktop_folder():
    path = os.path.join(os.path.expanduser("~"), "Desktop")
    os.startfile(path); return "Desktop folder khol diya!"

def take_quick_note(text: str):
    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(os.path.expanduser("~"), "Documents", f"FridayNote_{ts}.txt")
    with open(path, 'w', encoding='utf-8') as f: f.write(text)
    os.startfile(path)
    return f"Note save karke khol diya: {path}"

# ============================================================
#  8. PRODUCTIVITY
# ============================================================

def get_current_time():
    now = datetime.datetime.now()
    return f"Time: {now.strftime('%I:%M %p')} | Date: {now.strftime('%A, %d %B %Y')}"

def set_alarm(hour: int, minute: int, message: str = "Boss, alarm!"):
    def _alarm():
        now   = datetime.datetime.now()
        alarm = now.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        if alarm <= now: alarm += datetime.timedelta(days=1)
        time.sleep((alarm - now).total_seconds())
        import winsound
        from voice import speak
        speak(f"Boss! Alarm! {message}")
        for _ in range(3): winsound.Beep(1000, 600); time.sleep(0.2)
    threading.Thread(target=_alarm, daemon=True).start()
    return f"Alarm set: {int(hour):02d}:{int(minute):02d} — '{message}'"

_stopwatch_start = None
def start_stopwatch():
    global _stopwatch_start
    _stopwatch_start = time.time()
    return "Stopwatch start! 'stopwatch stop' bolo results ke liye."

def stop_stopwatch():
    global _stopwatch_start
    if _stopwatch_start is None: return "Stopwatch start nahi tha."
    elapsed = time.time() - _stopwatch_start
    _stopwatch_start = None
    m, s = divmod(int(elapsed), 60)
    h, m = divmod(m, 60)
    return f"Stopwatch stopped: {h:02d}:{m:02d}:{s:02d}"

_timer_thread = None
def start_timer(minutes: float, message: str = "Timer done!"):
    def _t():
        time.sleep(float(minutes) * 60)
        from voice import speak
        speak(f"Boss! {message} — {minutes} minute timer complete!")
        import winsound
        for _ in range(3): winsound.Beep(800, 500); time.sleep(0.3)
    threading.Thread(target=_t, daemon=True).start()
    return f"{minutes} minute timer set kar diya, Boss!"

_pomodoro_active = False
def start_pomodoro(work_min: int = 25, break_min: int = 5):
    global _pomodoro_active
    _pomodoro_active = True
    def _pomo():
        session = 1
        while _pomodoro_active:
            from voice import speak
            speak(f"Boss! Pomodoro session {session} shuru! {work_min} minute focus karo.")
            time.sleep(work_min * 60)
            if not _pomodoro_active: break
            speak(f"Session {session} done! {break_min} minute break lo, Boss!")
            time.sleep(break_min * 60)
            session += 1
    threading.Thread(target=_pomo, daemon=True).start()
    return f"Pomodoro shuru! {work_min}min work + {break_min}min break cycle."

def stop_pomodoro():
    global _pomodoro_active
    _pomodoro_active = False
    return "Pomodoro band kar diya, Boss!"

def add_calendar_event(title: str, date_str: str = ""):
    url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={title.replace(' ','+')}"
    if date_str: url += f"&dates={date_str}"
    webbrowser.open(url)
    return f"Google Calendar mein '{title}' event open kar diya!"

def open_todo():
    subprocess.Popen("start ms-todo:", shell=True)
    return "Microsoft To-Do khol diya!"

def type_text(text: str):
    import pyautogui
    time.sleep(1.5)
    pyautogui.write(text, interval=0.04)
    return f"Type kar diya!"

def send_email(to: str, subject: str = "", body: str = ""):
    import urllib.parse
    url = f"mailto:{to}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
    webbrowser.open(url)
    return f"Email draft {to} ke liye khol diya!"

def open_whatsapp(contact: str = ""):
    if contact:
        # Try WhatsApp web
        webbrowser.open(f"https://wa.me/{contact}")
    else:
        subprocess.Popen("whatsapp:", shell=True)
    return "WhatsApp khol diya!"

def calculator(expression: str):
    try:
        # Safe eval
        allowed = set('0123456789+-*/().% ')
        if all(c in allowed for c in expression):
            result = eval(expression)
            return f"{expression} = {result}"
        return "Unsafe expression."
    except Exception as e:
        return f"Calculation error: {e}"

def currency_convert(amount: float, from_cur: str, to_cur: str):
    webbrowser.open(f"https://www.google.com/search?q={amount}+{from_cur}+to+{to_cur}")
    return f"{amount} {from_cur} → {to_cur} conversion Google pe khol diya!"

def unit_convert(value: float, from_unit: str, to_unit: str):
    webbrowser.open(f"https://www.google.com/search?q={value}+{from_unit}+to+{to_unit}")
    return f"{value} {from_unit} → {to_unit} conversion Google pe open kiya!"

def translate_text(text: str, target: str = "en"):
    webbrowser.open(f"https://translate.google.com/?sl=auto&tl={target}&text={text.replace(' ','%20')}&op=translate")
    return "Translation Google Translate mein khol diya!"

def define_word(word: str):
    webbrowser.open(f"https://www.google.com/search?q=define+{word}")
    return f"'{word}' ki definition Google pe khol diya!"

def find_synonyms(word: str):
    webbrowser.open(f"https://www.thesaurus.com/browse/{word}")
    return f"'{word}' ke synonyms Thesaurus pe khol diye!"

def text_to_speech_file(text: str):
    """Save text as MP3"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        ts     = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path   = os.path.join(os.path.expanduser("~"), "Documents", f"Friday_TTS_{ts}.mp3")
        engine.save_to_file(text, path)
        engine.runAndWait()
        return f"Audio file save kar diya: {path}"
    except Exception as e:
        return f"TTS error: {e}"

def open_pdf(path: str):
    path = path.strip('"')
    if os.path.exists(path):
        os.startfile(path); return f"PDF khol diya: {path}"
    return "PDF file nahi mili."

def find_text_in_image(image_path: str):
    try:
        import pytesseract
        from PIL import Image
        text = pytesseract.image_to_string(Image.open(image_path))
        return f"Image mein milaa text:\n{text[:500]}"
    except:
        return "OCR ke liye Tesseract install karo: https://github.com/UB-Mannheim/tesseract/wiki"

def open_excel_helper():
    webbrowser.open("https://support.microsoft.com/excel"); return "Excel help khol di!"

def open_word_helper():
    webbrowser.open("https://support.microsoft.com/word"); return "Word help khol di!"

def open_ppt_helper():
    webbrowser.open("https://support.microsoft.com/powerpoint"); return "PowerPoint help khol di!"

def make_invoice():
    webbrowser.open("https://invoice-generator.com")
    return "Free invoice generator khol diya, Boss!"

def sign_document():
    webbrowser.open("https://www.docusign.com/esignature/sign-a-document")
    return "DocuSign khol diya document sign karne ke liye!"

def play_relax_sounds():
    webbrowser.open("https://www.noisli.com")
    return "Relaxing sounds Noisli pe khol diye! 🌿"

def play_focus_music():
    webbrowser.open("https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ")
    return "Focus music Spotify pe khol di, Boss! 🎵"

def block_website(domain: str):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    try:
        with open(hosts_path, 'a') as f:
            f.write(f"\n127.0.0.1 {domain}\n127.0.0.1 www.{domain}\n")
        return f"{domain} block kar diya, Boss!"
    except:
        return f"Admin rights chahiye hosts file edit karne ke liye. notepad ko Run as Administrator se chalao."

# ============================================================
#  9. DEVELOPER TOOLS
# ============================================================

def run_python_code(code: str):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code); tmp = f.name
    result = subprocess.run(['python', tmp], capture_output=True, text=True, timeout=30)
    os.unlink(tmp)
    out = (result.stdout or result.stderr or "No output").strip()
    return out[:800]

def git_command(cmd: str, repo_path: str = "."):
    result = subprocess.run(f'git {cmd}', capture_output=True, text=True, shell=True,
                            cwd=repo_path if os.path.exists(repo_path) else ".")
    return (result.stdout or result.stderr or "Done").strip()[:500]

def open_vscode(path: str = "."):
    subprocess.Popen(f'code "{path}"', shell=True)
    return f"VSCode mein khola: {path}"

def run_cmd(command: str):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, timeout=30)
        out = (result.stdout or result.stderr or "Done").strip()
        return out[:800]
    except subprocess.TimeoutExpired:
        return "Command timeout (30s)"
    except Exception as e:
        return f"Error: {e}"

def format_code(code: str, lang: str = "python"):
    if lang == "python":
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code); tmp = f.name
        subprocess.run(f'black "{tmp}"', shell=True, capture_output=True)
        with open(tmp, encoding='utf-8') as f: formatted = f.read()
        os.unlink(tmp)
        return formatted
    return "Formatting: install black (pip install black) for Python formatting."

def check_docker():
    result = subprocess.run("docker ps", capture_output=True, text=True, shell=True)
    return result.stdout or result.stderr or "Docker not running."

def open_db_tool():
    # Try common DB tools
    for app in ["DBeaver", "TablePlus", "HeidiSQL", "pgAdmin 4"]:
        try:
            subprocess.Popen(app, shell=True)
            return f"{app} khol diya!"
        except: pass
    webbrowser.open("https://dbeaver.io"); return "DBeaver download page khol diya!"

def deploy_info():
    webbrowser.open("https://railway.app"); return "Railway.app (free deploy) khol diya!"

def aws_console():
    webbrowser.open("https://console.aws.amazon.com"); return "AWS Console khol diya!"

# ============================================================
#  10. WEB & MEDIA
# ============================================================

def web_search(query: str):
    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ','+')}"); return f"'{query}' Google pe search kiya!"

def get_weather(city: str):
    try:
        import requests as req
        r = req.get(f"https://wttr.in/{city.replace(' ','+')}?format=3", timeout=5)
        return r.text.strip()
    except:
        webbrowser.open(f"https://weather.com/weather/today/l/{city.replace(' ','%20')}")
        return f"{city} weather browser mein khol diya."

def get_news():
    webbrowser.open("https://news.google.com"); return "Google News khol diya, Boss!"

def play_youtube(query: str):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ','+')}"); return f"YouTube pe '{query}' search kiya!"

def play_spotify(query: str):
    try: os.startfile(f"spotify:search:{query}")
    except: webbrowser.open(f"https://open.spotify.com/search/{query.replace(' ','%20')}")
    return f"Spotify pe '{query}' search kiya!"

def search_images(query: str):
    webbrowser.open(f"https://images.google.com/search?q={query.replace(' ','+')}"); return f"'{query}' images Google pe khol diye!"

def get_movie_info(title: str):
    webbrowser.open(f"https://www.imdb.com/find?q={title.replace(' ','+')}"); return f"'{title}' IMDB pe khol diya!"

def get_book_info(title: str):
    webbrowser.open(f"https://www.goodreads.com/search?q={title.replace(' ','+')}"); return f"'{title}' Goodreads pe khol diya!"

def check_flight(flight: str):
    webbrowser.open(f"https://www.google.com/search?q={flight}+flight+status"); return f"Flight {flight} status search kiya!"

def search_hotels(city: str):
    webbrowser.open(f"https://www.booking.com/search.html?ss={city.replace(' ','+')}"); return f"{city} hotels Booking.com pe khol diye!"

def open_maps(destination: str):
    webbrowser.open(f"https://www.google.com/maps/search/{destination.replace(' ','+')}"); return f"'{destination}' Google Maps pe khol diya!"

def order_food():
    webbrowser.open("https://www.swiggy.com"); return "Swiggy khol diya, Boss! 🍕"

def shop_online(query: str):
    webbrowser.open(f"https://www.amazon.in/s?k={query.replace(' ','+')}"); return f"'{query}' Amazon pe search kiya!"

def track_package(tracking_id: str):
    webbrowser.open(f"https://www.google.com/search?q=track+package+{tracking_id}"); return f"Package {tracking_id} track karne ki koshish ki!"

def check_stock(symbol: str):
    webbrowser.open(f"https://finance.yahoo.com/quote/{symbol.upper()}"); return f"{symbol.upper()} stock Yahoo Finance pe khol diya!"

def check_crypto(symbol: str):
    webbrowser.open(f"https://coinmarketcap.com/currencies/{symbol.lower()}"); return f"{symbol} crypto CoinMarketCap pe khol diya!"

def get_sports_scores(team: str = ""):
    query = f"{team}+live+score" if team else "live+cricket+scores"
    webbrowser.open(f"https://www.google.com/search?q={query}"); return "Sports scores Google pe khol diye!"

def tell_joke():
    import random
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
        "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
        "Why was the math book sad? It had too many problems.",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "Boss, why don't scientists trust atoms? Because they make up everything! 😂",
        "Debugging: Removing the needles from the haystack. Programming: Putting them back.",
    ]
    return random.choice(jokes)

def get_daily_quote():
    try:
        import requests as req
        r = req.get("https://zenquotes.io/api/random", timeout=5)
        data = r.json()[0]
        return f'"{data["q"]}" — {data["a"]}'
    except:
        quotes = [
            '"Sometimes you gotta run before you can walk." — Tony Stark',
            '"The secret of getting ahead is getting started." — Mark Twain',
            '"Code is like humor. When you have to explain it, it\'s bad." — Cory House',
        ]
        import random; return random.choice(quotes)

def get_meditation():
    webbrowser.open("https://www.youtube.com/results?search_query=10+minute+guided+meditation")
    return "Guided meditation YouTube pe khol diya, Boss. Relax karo! 🧘"

def get_workout_plan():
    webbrowser.open("https://www.youtube.com/results?search_query=home+workout+plan+beginner")
    return "Workout videos YouTube pe khol diye, Boss! 💪"

def get_diet_plan():
    webbrowser.open("https://www.healthline.com/nutrition/healthy-eating-for-beginners")
    return "Diet plan Healthline pe khol diya!"

def find_recipe(dish: str):
    webbrowser.open(f"https://www.google.com/search?q={dish.replace(' ','+')}+recipe")
    return f"'{dish}' recipe Google pe khol diya! 🍳"

def get_pet_care(pet: str):
    webbrowser.open(f"https://www.petmd.com/search?q={pet.replace(' ','+')}+care")
    return f"{pet} care tips PetMD pe khol diye!"

def get_plant_care(plant: str):
    webbrowser.open(f"https://www.google.com/search?q={plant.replace(' ','+')}+plant+care+tips")
    return f"{plant} plant care tips khol diye!"

def get_car_info(model: str):
    webbrowser.open(f"https://www.google.com/search?q={model.replace(' ','+')}+car+specs+review")
    return f"{model} car info Google pe khol diya!"

def get_home_decor():
    webbrowser.open("https://www.pinterest.com/search/pins/?q=home+decor+ideas")
    return "Home decor ideas Pinterest pe khol diye! 🏠"

def get_fashion_tips():
    webbrowser.open("https://www.gq.com/style/fashion"); return "Fashion tips GQ pe khol diye!"

def get_wine_pairing(food: str):
    webbrowser.open(f"https://www.google.com/search?q=wine+pairing+with+{food.replace(' ','+')}"); return f"{food} ke liye wine pairing tips khol diye!"

# ============================================================
#  MASTER TOOLS REGISTRY
# ============================================================

TOOLS = {
    # System
    "system_info":        (get_system_info,        []),
    "shutdown":           (shutdown_pc,             []),
    "restart":            (restart_pc,              []),
    "lock":               (lock_screen,             []),
    "logout":             (logout_user,             []),
    "sleep":              (sleep_pc,                []),
    "sync_time":          (sync_time,               []),
    "game_mode_on":       (enable_game_mode,        []),
    "game_mode_off":      (disable_game_mode,       []),
    "task_manager":       (open_task_manager,       []),
    "auto_update":        (auto_update,             []),
    "phone_link":         (open_phone_link,         []),
    "virus_scan":         (virus_scan,              []),
    "clean_temp":         (clean_temp_files,        []),
    "empty_trash":        (empty_recycle_bin,       []),
    "battery":            (get_battery_info,        []),
    "battery_saver":      (enable_battery_saver,   []),
    "cpu_temp":           (get_cpu_temp,            []),
    "network_speed":      (check_network_speed,     []),
    "wifi_info":          (get_wifi_info,           []),
    "wifi_settings":      (open_wifi_settings,      []),
    "bluetooth":          (open_bluetooth_settings, []),
    "printer":            (open_printer_settings,   []),

    # Audio
    "volume":             (set_volume,             ["level"]),
    "mute":               (mute_volume,            []),
    "unmute":             (unmute_volume,          []),
    "mute_mic":           (mute_mic,               []),
    "unmute_mic":         (unmute_mic,             []),

    # Display
    "brightness":         (set_brightness,         ["level"]),
    "night_mode":         (enable_night_mode,      []),
    "light_mode":         (enable_light_mode,      []),
    "eye_care":           (enable_eye_care,        []),
    "color_picker":       (open_color_picker,      []),

    # Screenshot/Screen
    "screenshot":         (take_screenshot,        []),
    "snipping_tool":      (open_snipping_tool,     []),
    "screen_record":      (start_screen_recording, []),
    "stop_record":        (stop_screen_recording,  []),

    # Mouse/Keyboard
    "mouse_speed":        (set_mouse_speed,        ["speed"]),

    # Files & Apps
    "open_app":           (open_app,               ["app_name"]),
    "open_file":          (open_file,              ["path"]),
    "search_file":        (search_file,            ["name"]),
    "create_folder":      (create_folder,          ["path"]),
    "delete_file":        (delete_file,            ["path"]),
    "rename_file":        (rename_file,            ["old_path","new_name"]),
    "shred_file":         (shred_file,             ["path"]),
    "zip":                (zip_files,              ["files_str","output"]),
    "unzip":              (unzip_file,             ["zip_path"]),
    "hide_file":          (hide_file,              ["path"]),
    "show_hidden":        (show_hidden_files,      []),
    "copy_path":          (copy_path,              ["path"]),
    "folder_size":        (get_folder_size,        ["path"]),
    "make_shortcut":      (make_shortcut,          ["target"]),
    "wallpaper":          (change_wallpaper,       ["path"]),
    "hide_desktop":       (hide_desktop_icons,     []),
    "refresh_desktop":    (refresh_desktop,        []),
    "snap_left":          (snap_window_left,       []),
    "snap_right":         (snap_window_right,      []),
    "pin_top":            (pin_window_on_top,      []),
    "clipboard_history":  (open_clipboard_history, []),
    "clipboard_get":      (get_clipboard,          []),
    "clipboard_set":      (set_clipboard,          ["text"]),
    "downloads":          (open_downloads,         []),
    "desktop":            (open_desktop_folder,    []),
    "quick_note":         (take_quick_note,        ["text"]),

    # Productivity
    "time":               (get_current_time,       []),
    "alarm":              (set_alarm,              ["hour","minute"]),
    "stopwatch_start":    (start_stopwatch,        []),
    "stopwatch_stop":     (stop_stopwatch,         []),
    "timer":              (start_timer,            ["minutes"]),
    "pomodoro_start":     (start_pomodoro,         []),
    "pomodoro_stop":      (stop_pomodoro,          []),
    "add_event":          (add_calendar_event,     ["title"]),
    "todo":               (open_todo,              []),
    "type":               (type_text,              ["text"]),
    "email":              (send_email,             ["to"]),
    "whatsapp":           (open_whatsapp,          []),
    "calculator":         (calculator,             ["expression"]),
    "currency":           (currency_convert,       ["amount","from_cur","to_cur"]),
    "unit_convert":       (unit_convert,           ["value","from_unit","to_unit"]),
    "translate":          (translate_text,         ["text"]),
    "define":             (define_word,            ["word"]),
    "synonyms":           (find_synonyms,          ["word"]),
    "tts_file":           (text_to_speech_file,    ["text"]),
    "open_pdf":           (open_pdf,               ["path"]),
    "ocr":                (find_text_in_image,     ["image_path"]),
    "excel_help":         (open_excel_helper,      []),
    "word_help":          (open_word_helper,       []),
    "ppt_help":           (open_ppt_helper,        []),
    "invoice":            (make_invoice,           []),
    "sign_doc":           (sign_document,          []),
    "relax":              (play_relax_sounds,      []),
    "focus_music":        (play_focus_music,       []),
    "block_site":         (block_website,          ["domain"]),

    # Developer
    "run_python":         (run_python_code,        ["code"]),
    "git":                (git_command,            ["cmd"]),
    "vscode":             (open_vscode,            []),
    "run_cmd":            (run_cmd,                ["command"]),
    "format_code":        (format_code,            ["code"]),
    "docker":             (check_docker,           []),
    "db_tool":            (open_db_tool,           []),
    "deploy":             (deploy_info,            []),
    "aws":                (aws_console,            []),

    # Web & Media
    "search":             (web_search,             ["query"]),
    "weather":            (get_weather,            ["city"]),
    "news":               (get_news,               []),
    "youtube":            (play_youtube,           ["query"]),
    "spotify":            (play_spotify,           ["query"]),
    "images":             (search_images,          ["query"]),
    "movie":              (get_movie_info,         ["title"]),
    "book":               (get_book_info,          ["title"]),
    "flight":             (check_flight,           ["flight"]),
    "hotels":             (search_hotels,          ["city"]),
    "maps":               (open_maps,              ["destination"]),
    "food_delivery":      (order_food,             []),
    "shop":               (shop_online,            ["query"]),
    "track_package":      (track_package,          ["tracking_id"]),
    "stock":              (check_stock,            ["symbol"]),
    "crypto":             (check_crypto,           ["symbol"]),
    "sports":             (get_sports_scores,      []),
    "joke":               (tell_joke,              []),
    "quote":              (get_daily_quote,        []),
    "meditation":         (get_meditation,         []),
    "workout":            (get_workout_plan,       []),
    "diet":               (get_diet_plan,          []),
    "recipe":             (find_recipe,            ["dish"]),
    "pet_care":           (get_pet_care,           ["pet"]),
    "plant_care":         (get_plant_care,         ["plant"]),
    "car_info":           (get_car_info,           ["model"]),
    "home_decor":         (get_home_decor,         []),
    "fashion":            (get_fashion_tips,       []),
    "wine":               (get_wine_pairing,       ["food"]),
}

def run_tool(name: str, args: dict):
    """Tool ko args ke saath run karo"""
    if name not in TOOLS:
        return None
    func, _ = TOOLS[name]
    try:
        if args:
            return func(**args)
        return func()
    except TypeError as e:
        # Try without args
        try: return func()
        except: return f"Tool error: {e}"
    except Exception as e:
        return f"Tool error: {e}"