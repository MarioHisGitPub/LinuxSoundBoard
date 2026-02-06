# LinuxSoundBoard.py — Full version with centered loader and proper progress
import os
import sys
import subprocess
import importlib
import time
import threading

# ------------------- Automatic dependency installer -------------------
required_packages = ["customtkinter", "Pillow", "pynput", "distro"]

for pkg in required_packages:
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# ------------------- Import CustomTkinter early -------------------
import customtkinter as ctk

# ------------------- Loader -------------------
def show_loader():
    loader = ctk.CTk()
    loader.title("Loading")
    loader.geometry("400x120")
    loader.resizable(False, False)
    loader.configure(fg_color="#12151c")
    loader.overrideredirect(True)

    label = ctk.CTkLabel(
        loader,
        text="Detecting audio system...",
        text_color="white",
        font=("Segoe UI", 16, "bold")
    )
    label.pack(pady=20)

    progress = ctk.CTkProgressBar(loader, width=350)
    progress.set(0)
    progress.pack(pady=10)

    loader.update_idletasks()
    w, h = loader.winfo_width(), loader.winfo_height()
    x = (loader.winfo_screenwidth() // 2) - (w // 2)
    y = (loader.winfo_screenheight() // 2) - (h // 2)
    loader.geometry(f"{w}x{h}+{x}+{y}")

    loader.update()
    return loader, label, progress

loader, loader_label, loader_bar = show_loader()

loader_label.configure(text="Checking dependencies...")
loader_bar.set(0.2)
loader.update()
time.sleep(0.2)

# ------------------- Imports -------------------
from PIL import Image
import webbrowser
from tkinter import filedialog, messagebox
import backend
import distro

# ------------------- Backend init -------------------
def backend_init_with_loader():
    loader_label.configure(text="Checking PulseAudio...")
    loader_bar.set(0.4)
    loader.update()
    backend.init_dependencies()

    loader_label.configure(text="Starting hotkey listener...")
    loader_bar.set(0.7)
    loader.update()
    backend.start_hotkey_listener()

    loader_label.configure(text="Preparing soundboard...")
    loader_bar.set(1.0)
    loader.update()
    time.sleep(0.5)

backend_init_with_loader()

# ------------------- Detect Linux Distro (UNCHANGED) -------------------
detected_id = distro.id()
DISTRO_MAP = {
    "debian": "Debian",
    "ubuntu": "Debian",
    "pop": "Debian",
    "linuxmint": "Debian",
    "elementary": "Debian",
    "kali": "Debian",
    "deepin": "Debian",
    "devuan": "Debian",

    "fedora": "Fedora",
    "rhel": "Fedora",
    "centos": "Fedora",
    "rocky": "Fedora",
    "almalinux": "Fedora",

    "arch": "Arch",
    "manjaro": "Arch",
    "endeavouros": "Arch",

    "opensuse": "openSUSE",
    "suse": "openSUSE",

    "gentoo": "Gentoo",
    "calculate": "Gentoo",

    "slackware": "Slackware",
    "alpine": "Alpine",

    "void": "Void",
    "solus": "Solus",
    "nixos": "NixOS",
}

user_distro = DISTRO_MAP.get(detected_id, "Debian")
loader.destroy()

# ------------------- Appearance -------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ------------------- Colors -------------------
APP_BG = "#12151c"
PANEL = "#1f2a38"
BUTTON = "#2c3e50"
BUTTON_HOVER = "#5dade2"
TOGGLE_ON = "#5dade2"
TOGGLE_OFF = "#c0392b"
TEXT = "white"

# ------------------- Root -------------------
root = ctk.CTk()
root.title(f"{user_distro} Soundboard")
root.geometry("1150x680")
root.resizable(False, False)
root.configure(fg_color=APP_BG)

# ------------------- Topbar -------------------
topbar = ctk.CTkFrame(root, fg_color=APP_BG)
topbar.pack(fill="x", pady=10, padx=15)

# Logo
try:
    logo_path = backend.resource_path("logo.png")
    if os.path.isfile(logo_path):
        img = Image.open(logo_path).convert("RGBA").resize((100, 100))
        logo = ctk.CTkImage(img, size=(100, 100))
        ctk.CTkLabel(topbar, image=logo, text="").pack(side="right", padx=20)
except:
    pass

# Donate
try:
    donate_path = backend.resource_path("paypal-donate-button.png")
    if os.path.isfile(donate_path):
        img = Image.open(donate_path).resize((180, 70))
        donate_img = ctk.CTkImage(img, size=(180, 70))
        ctk.CTkButton(
            topbar,
            image=donate_img,
            text="",
            fg_color="transparent",
            hover=False,
            command=lambda: webbrowser.open("https://www.paypal.me/Depretre")
        ).pack(side="left", padx=5)
except:
    pass

# Title
title_frame = ctk.CTkFrame(topbar, fg_color="transparent")
title_frame.pack(side="left", expand=True)

ctk.CTkLabel(
    title_frame,
    text=f"{user_distro} Soundboard",
    text_color=TOGGLE_ON,
    font=("Segoe UI", 28, "bold")
).pack(pady=(0, 5))

ctk.CTkLabel(
    title_frame,
    text=f"Detected OS: {detected_id}",
    text_color=BUTTON_HOVER,
    font=("Segoe UI", 16, "italic")
).pack()

# ------------------- Toggle -------------------
def toggle_soundboard():
    backend.soundboard_on = not backend.soundboard_on
    toggle_btn.configure(
        text="Soundboard Enabled" if backend.soundboard_on else "Soundboard Disabled",
        fg_color=TOGGLE_ON if backend.soundboard_on else TOGGLE_OFF
    )

toggle_btn = ctk.CTkButton(
    root,
    text="Soundboard Enabled",
    fg_color=TOGGLE_ON,
    hover_color=BUTTON_HOVER,
    font=("Segoe UI", 16, "bold"),
    width=250,
    height=50,
    corner_radius=12,
    command=toggle_soundboard
)
toggle_btn.pack(pady=15)

# ------------------- Sound list -------------------
scroll_frame = ctk.CTkScrollableFrame(root, fg_color=APP_BG)
scroll_frame.pack(fill="both", expand=True, padx=15, pady=10)

labels = {}

def update_label(sound_key):
    mp3 = os.path.basename(backend.MP3S[sound_key])
    mapped = [k for k, v in backend.KEY_MAP.items() if v == sound_key]
    labels[sound_key].configure(text=f"{mp3}   |   Key: {mapped[0] if mapped else '?'}")

def change_mp3(sound_key):
    f = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if f:
        backend.MP3S[sound_key] = f
        update_label(sound_key)

def change_key(sound_key):
    messagebox.showinfo("Key Mapping", f"Press a key for {sound_key.upper()}…")
    chosen = {}
    from pynput.keyboard import Listener
    def on_press(key):
        chosen["key"] = key
        return False
    with Listener(on_press=on_press) as l:
        l.join()
    key_str = backend.key_to_str(chosen["key"])
    backend.KEY_MAP = {k: v for k, v in backend.KEY_MAP.items() if v != sound_key}
    backend.KEY_MAP[key_str] = sound_key
    update_label(sound_key)

# Rows
for sound_key in backend.MP3S:
    row = ctk.CTkFrame(scroll_frame, fg_color=PANEL, corner_radius=12)
    row.pack(fill="x", pady=6, padx=6)


    lbl = ctk.CTkLabel(row, text="", text_color=TEXT, anchor="w", font=("Segoe UI", 14))
    lbl.pack(side="left", padx=20, pady=10, fill="both", expand=True)
    labels[sound_key] = lbl
    update_label(sound_key)

    ctk.CTkButton(
        row,
        text="Change MP3",
        fg_color=BUTTON,
        hover_color=BUTTON_HOVER,
        text_color=TEXT,
        corner_radius=12,
        width=130,
        height=38,
        command=lambda k=sound_key: change_mp3(k)
    ).pack(side="right", padx=5, pady=8)

    ctk.CTkButton(
        row,
        text="Map Key",
        fg_color=BUTTON,
        hover_color=BUTTON_HOVER,
        text_color=TEXT,
        corner_radius=12,
        width=130,
        height=38,
        command=lambda k=sound_key: change_key(k)
    ).pack(side="right", padx=5, pady=8)

root.mainloop()
