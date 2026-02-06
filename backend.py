# backend.py — FIXED LINUX VERSION + AUTO PULSEAUDIO INSTALL + EXECUTABLE PERMISSION
import os
import sys
import subprocess
import shutil
import threading
from pynput.keyboard import Key, Listener as kbListener, KeyCode

# ------------------- Helper -------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        # Base path is always the folder of this script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "assets", relative_path)

# ------------------- Detect Linux Distro -------------------
try:
    import distro
    detected_id = distro.id()
except ImportError:
    detected_id = "debian"

DISTRO_MAP = {
    "debian": "Debian",
    "ubuntu": "Debian",
    "pop": "Debian",
    "linuxmint": "Debian",
    "fedora": "Fedora",
    "rhel": "Fedora",
    "centos": "Fedora",
    "arch": "Arch",
    "manjaro": "Arch",
    "opensuse": "openSUSE"
}

MAIN_DISTRO = DISTRO_MAP.get(detected_id, "Debian")

# ------------------- Dependency check & auto-install -------------------
def install_pulseaudio():
    if shutil.which("pactl") and shutil.which("paplay"):
        print("[+] PulseAudio already installed, skipping installation.")
        return  # already installed

    print(f"[!] PulseAudio missing → installing for {MAIN_DISTRO}...")
    try:
        if MAIN_DISTRO == "Debian":
            subprocess.check_call(["sudo", "apt", "update"])
            subprocess.check_call(["sudo", "apt", "install", "-y", "pulseaudio", "pulseaudio-utils"])
        elif MAIN_DISTRO == "Fedora":
            subprocess.check_call(["sudo", "dnf", "install", "-y", "pulseaudio", "pulseaudio-utils"])
        elif MAIN_DISTRO == "Arch":
            subprocess.check_call(["sudo", "pacman", "-Syu", "--noconfirm", "pulseaudio"])
        elif MAIN_DISTRO == "openSUSE":
            subprocess.check_call(["sudo", "zypper", "install", "-y", "pulseaudio", "pulseaudio-utils"])
    except Exception as e:
        print(f"[!] Failed to install PulseAudio automatically: {e}")
        sys.exit(1)

def check_dependency(cmd, name, packages=None):
    import tkinter as tk
    from tkinter import messagebox

    if shutil.which(cmd) is None:
        root = tk.Tk()
        root.withdraw()
        pkg_str = ", ".join(packages) if packages else cmd
        messagebox.showinfo(
            "Missing dependency",
            f"{name} ({cmd}) is missing.\n\nPlease install: {pkg_str}"
        )
        sys.exit(0)

def init_dependencies():
    # Install PulseAudio if missing
    install_pulseaudio()

    check_dependency("mpv", "MPV Media Player", ["mpv"])
    check_dependency("pactl", "PulseAudio control tool", ["pulseaudio-utils"])
    check_dependency("paplay", "PulseAudio playback utility", ["pulseaudio-utils"])

# ------------------- State -------------------
soundboard_on = True
active_processes = {}

# ------------------- Key → string -------------------
def key_to_str(key):
    if isinstance(key, Key):
        return str(key).replace("Key.", "").lower()
    if isinstance(key, KeyCode):
        if key.char:
            return key.char.lower()
    return str(key).lower()

# ------------------- Defaults -------------------
WRAPPER = resource_path("Linux.sh")
CHEWBACCA = resource_path("chewbacca.mp3")

# Make sure Linux.sh is executable
if not os.access(WRAPPER, os.X_OK):
    os.chmod(WRAPPER, 0o755)

# F1–F12 default sounds
MP3S = {f"f{i}": CHEWBACCA for i in range(1, 13)}
KEY_MAP = {f"f{i}": f"f{i}" for i in range(1, 13)}

# ------------------- Playback -------------------
def play_sound(mapped_key):
    global soundboard_on
    if not soundboard_on:
        return

    mp3_path = MP3S.get(mapped_key, "")
    if not os.path.isfile(mp3_path):
        print(f"MP3 missing: {mp3_path}")
        return

    # Stop currently playing sound for this key
    if mapped_key in active_processes:
        proc = active_processes[mapped_key]
        if proc.poll() is None:
            proc.terminate()

    # Start the script via bash
    print(f"Playing {mp3_path} (key {mapped_key}) on {MAIN_DISTRO}")
    proc = subprocess.Popen(["bash", WRAPPER, mp3_path])
    active_processes[mapped_key] = proc

# ------------------- Hotkey listener -------------------
def start_hotkey_listener():
    def on_release(key):
        kstr = key_to_str(key)
        mapped = KEY_MAP.get(kstr)
        if mapped:
            play_sound(mapped)

    threading.Thread(target=lambda: kbListener(on_release=on_release).run(), daemon=True).start()
