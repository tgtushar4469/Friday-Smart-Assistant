# ============================================================
#   FRIDAY AI v2.0 — main.py
#   Iron Man style GUI — run this file!
# ============================================================

import sys, threading, datetime, os
import tkinter as tk
from tkinter import scrolledtext, ttk

from config import ASSISTANT_NAME, USER_NAME, WAKE_WORD, GROQ_API_KEY
from voice import speak
from wake_word import start_wake_detection, listen_once
from brain import process_command, get_greeting, clear_memory

# ──────────────────────────────────────────────────────────────
#  COLORS
# ──────────────────────────────────────────────────────────────
BG      = "#070b14"
BG2     = "#0d1321"
BG3     = "#111827"
ACCENT  = "#00c8ff"
ACCENT2 = "#0066ff"
ORANGE  = "#ff8c00"
GREEN   = "#00ff9f"
RED     = "#ff3c3c"
YELLOW  = "#ffd700"
GRAY    = "#2a3550"
TEXT    = "#d0e8ff"
DIM     = "#3a4f6a"

QUICK_CMDS = [
    ("⚡ Info",      "system info batao"),
    ("🔊 Vol 60",    "volume 60 karo"),
    ("📸 Shot",      "screenshot lo"),
    ("🌙 Dark",      "dark mode on karo"),
    ("🧹 Clean",     "temp files clean karo"),
    ("🔋 Battery",   "battery status batao"),
    ("🌐 News",      "latest news dikhao"),
    ("😄 Joke",      "ek joke sunao"),
    ("💡 Quote",     "aaj ka quote batao"),
    ("🔒 Lock",      "screen lock karo"),
    ("🎮 Game+",     "game mode on"),
    ("⏱️ Timer 25",  "25 minute timer set karo"),
]


class FridayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"⚡ {ASSISTANT_NAME}  —  AI Personal Assistant  |  Boss: {USER_NAME}")
        self.root.geometry("1000x720")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.root.minsize(800, 560)

        self.listening  = False
        self.pin_top    = tk.BooleanVar(value=False)

        self._setup_styles()
        self._build_ui()
        self._start()

    # ──────────────────────────────────────────────────────
    #  STYLES
    # ──────────────────────────────────────────────────────
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TScrollbar", background=BG3, troughcolor=BG2,
                         bordercolor=BG, arrowcolor=ACCENT, relief="flat")

    # ──────────────────────────────────────────────────────
    #  UI BUILD
    # ──────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header ─────────────────────────────────────────
        hdr = tk.Frame(self.root, bg=BG, pady=12)
        hdr.pack(fill=tk.X, padx=24)

        tk.Label(hdr, text="⚡ F.R.I.D.A.Y",
                 font=("Consolas",24,"bold"), fg=ACCENT, bg=BG).pack(side=tk.LEFT)
        tk.Label(hdr, text=f"   AI Personal Assistant  ·  Boss: {USER_NAME}",
                 font=("Consolas",10), fg=DIM, bg=BG).pack(side=tk.LEFT, pady=6)

        # Pin checkbox
        tk.Checkbutton(hdr, text="📌 Pin", variable=self.pin_top,
                       command=lambda: self.root.attributes("-topmost", self.pin_top.get()),
                       bg=BG, fg=DIM, selectcolor=BG, activebackground=BG,
                       font=("Consolas",9)).pack(side=tk.RIGHT, padx=6)

        # Status dot
        self.status_lbl = tk.Label(hdr, text="● BOOTING", font=("Consolas",10,"bold"),
                                    fg=YELLOW, bg=BG)
        self.status_lbl.pack(side=tk.RIGHT, padx=12)

        # Divider
        tk.Frame(self.root, bg=ACCENT, height=1).pack(fill=tk.X, padx=24)

        # ── Chat + Sidebar ──────────────────────────────────
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill=tk.BOTH, expand=True, padx=24, pady=8)

        # Chat
        self.chat = scrolledtext.ScrolledText(
            body, wrap=tk.WORD,
            font=("Consolas",11), bg=BG2, fg=TEXT,
            insertbackground=ACCENT, selectbackground=GRAY,
            relief=tk.FLAT, bd=0, padx=16, pady=12, state=tk.DISABLED)
        self.chat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tags
        self.chat.tag_config("fri_name",  foreground=ACCENT,  font=("Consolas",11,"bold"))
        self.chat.tag_config("fri_text",  foreground="#b8e0ff")
        self.chat.tag_config("usr_name",  foreground=ORANGE,  font=("Consolas",11,"bold"))
        self.chat.tag_config("usr_text",  foreground="#ffe8c0")
        self.chat.tag_config("sys_text",  foreground=DIM,     font=("Consolas",9))
        self.chat.tag_config("ts",        foreground="#2a4060",font=("Consolas",9))

        # Sidebar
        side = tk.Frame(body, bg=BG, width=180)
        side.pack(side=tk.RIGHT, fill=tk.Y, padx=(10,0))
        side.pack_propagate(False)

        tk.Label(side, text="QUICK ACTIONS", font=("Consolas",8,"bold"),
                 fg=DIM, bg=BG).pack(pady=(4,6))

        for label, cmd in QUICK_CMDS:
            tk.Button(side, text=label, font=("Consolas",9),
                      bg=BG3, fg=ACCENT, activebackground=GRAY,
                      relief=tk.FLAT, bd=0, pady=5, cursor="hand2",
                      command=lambda c=cmd: self._run(c)
                      ).pack(fill=tk.X, pady=2, padx=4)

        tk.Frame(side, bg=GRAY, height=1).pack(fill=tk.X, pady=8, padx=4)
        tk.Button(side, text="🗑 Clear Chat", font=("Consolas",9),
                  bg=BG3, fg=RED, activebackground=GRAY,
                  relief=tk.FLAT, bd=0, pady=5, cursor="hand2",
                  command=self._clear).pack(fill=tk.X, padx=4)

        # ── Input bar ──────────────────────────────────────
        inp_row = tk.Frame(self.root, bg=BG)
        inp_row.pack(fill=tk.X, padx=24, pady=(0,8))

        self.mic_btn = tk.Button(inp_row, text="🎤", font=("Arial",16),
                                  bg=BG3, fg=ACCENT, activebackground=ACCENT,
                                  activeforeground=BG, relief=tk.FLAT, width=3,
                                  cursor="hand2", command=self._voice_input)
        self.mic_btn.pack(side=tk.LEFT, padx=(0,6))

        self.inp = tk.Entry(inp_row, font=("Consolas",12),
                             bg=BG3, fg="white", insertbackground=ACCENT,
                             relief=tk.FLAT, bd=10)
        self.inp.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.inp.bind("<Return>", lambda e: self._submit())
        self.inp.focus()

        tk.Button(inp_row, text="  Send ➤  ", font=("Consolas",11,"bold"),
                  bg=ACCENT, fg=BG, activebackground=ACCENT2,
                  relief=tk.FLAT, padx=14, pady=7, cursor="hand2",
                  command=self._submit).pack(side=tk.LEFT, padx=(6,0))

        # ── Wake word hint ─────────────────────────────────
        tk.Label(self.root,
                 text=f'💬  Say  "{WAKE_WORD}"  to activate voice anytime  ·  or type below',
                 font=("Consolas",9), fg=DIM, bg=BG).pack(pady=(0,6))

    # ──────────────────────────────────────────────────────
    #  CHAT HELPERS
    # ──────────────────────────────────────────────────────
    def _add(self, sender, msg, name_tag, text_tag):
        self.chat.config(state=tk.NORMAL)
        ts = datetime.datetime.now().strftime("%H:%M")
        self.chat.insert(tk.END, f"\n[{ts}] ", "ts")
        self.chat.insert(tk.END, f"{sender}: ", name_tag)
        self.chat.insert(tk.END, f"{msg}\n",    text_tag)
        self.chat.config(state=tk.DISABLED)
        self.chat.see(tk.END)

    def _sys(self, msg):
        self.chat.config(state=tk.NORMAL)
        self.chat.insert(tk.END, f"  ▸ {msg}\n", "sys_text")
        self.chat.config(state=tk.DISABLED)
        self.chat.see(tk.END)

    def _status(self, txt, color):
        self.status_lbl.config(text=f"● {txt}", fg=color)

    def _clear(self):
        self.chat.config(state=tk.NORMAL)
        self.chat.delete(1.0, tk.END)
        self.chat.config(state=tk.DISABLED)
        clear_memory()
        self._sys("Memory & chat cleared. Fresh start, Boss!")

    # ──────────────────────────────────────────────────────
    #  COMMAND PROCESSING
    # ──────────────────────────────────────────────────────
    def _submit(self):
        text = self.inp.get().strip()
        if not text: return
        self.inp.delete(0, tk.END)
        self._run(text)

    def _run(self, cmd: str):
        self._add(USER_NAME, cmd, "usr_name", "usr_text")
        self._status("THINKING...", YELLOW)

        def _worker():
            try:
                reply = process_command(cmd)
                self._add(ASSISTANT_NAME, reply, "fri_name", "fri_text")
                self._status("ACTIVE", GREEN)
                threading.Thread(target=speak, args=(reply,), daemon=True).start()
            except Exception as e:
                self._add(ASSISTANT_NAME, f"Error: {e}", "fri_name", "fri_text")
                self._status("ERROR", RED)
            finally:
                self._status("LISTENING", ACCENT)

        threading.Thread(target=_worker, daemon=True).start()

    def _voice_input(self):
        if self.listening: return

        def _vt():
            self.listening = True
            self._status("LISTENING...", ORANGE)
            self.mic_btn.config(fg=RED, text="🔴")
            text = listen_once(timeout=12)
            self.mic_btn.config(fg=ACCENT, text="🎤")
            self.listening = False
            if text:
                self._run(text)
            else:
                self._sys("Kuch nahi suna. Dobara try karo.")
                self._status("LISTENING", ACCENT)

        threading.Thread(target=_vt, daemon=True).start()

    def _on_wake(self):
        self._sys(f'"{WAKE_WORD}" detected! Bol Boss...')
        speak("Yes Boss?", use_online=False)
        self._voice_input()

    # ──────────────────────────────────────────────────────
    #  STARTUP
    # ──────────────────────────────────────────────────────
    def _start(self):
        def _boot():
            if GROQ_API_KEY == "YAHAN_APNI_GROQ_KEY_DAALO":
                self._sys("⚠️  config.py mein Groq API key daalo!")
                self._status("NO API KEY", RED)
                return

            self._sys("Friday AI v2.0 initializing...")
            self._sys(f"AI Model: Groq Llama 3.3 70B")
            self._sys("All 100+ capabilities loaded ✓")

            greeting = get_greeting()
            self._add(ASSISTANT_NAME, greeting, "fri_name", "fri_text")
            self._status("ACTIVE", GREEN)
            threading.Thread(target=speak, args=(greeting,), daemon=True).start()

            self._sys(f'Wake word detection active: "{WAKE_WORD}"')
            start_wake_detection(self._on_wake)
            self._status("LISTENING", ACCENT)

        threading.Thread(target=_boot, daemon=True).start()

    def run(self):
        self.root.mainloop()


# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 56)
    print("  ⚡ F.R.I.D.A.Y  AI Personal Assistant  v2.0")
    print(f"     For: {USER_NAME}")
    print("=" * 56)
    FridayApp().run()