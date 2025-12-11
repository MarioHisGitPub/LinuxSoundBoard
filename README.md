<!--
 _____ _   _ _     _     ____ _____  _    ____ _  _______ ____  
|  ___| | | | |   | |   / ___|_   _|/ \  / ___| |/ / ____|  _ \ 
| |_  | | | | |   | |   \___ \ | | / _ \| |   | ' /|  _| | | | |
| _| | |_| | |___| |___ ___) || |/ ___ \ |___| . \| |___| |_| |
|_|    \___/|_____|_____|____/ |_/_/   \_\____|_|\_\_____|____/ 
-->

# Linux Soundboard — README

## Overview
Linux Soundboard is a modern and professional soundboard for Linux.
All required files (MP3s, logo, donation button, shell script) are located in the `assets/` folder.

## Requirements
For proper audio playback, your system must have the following tools installed:
- MPV Media Player (`mpv`)
- PulseAudio control tool (`pactl`)
- PulseAudio playback utility (`paplay`)

On most Linux distributions, install them via:
sudo apt install mpv pulseaudio-utils

> The program will check if these dependencies are present at startup and show a message if anything is missing.

## Installation & Usage
1. Navigate to the folder containing the executable:
cd /path/to/SoundBoardApp/dist

2. Make the executable runnable:
chmod +x LinuxSoundBoard

3. Make sure the shell script is executable:
chmod +x ../assets/herbert_play.sh

> Adjust the path depending on where your `assets/` folder is relative to the executable.

4. Start the soundboard:
./LinuxSoundBoard

## Assets Folder
Ensure that the `assets/` folder is present next to the executable. This folder contains:
assets/
├─ *.mp3
├─ logo.png
├─ paypal-donate-button.png
├─ herbert_play.sh

## Ready to Use
No Python, pip, or additional dependencies are needed to run the executable, but PulseAudio and MPV must be installed.

## Optional Quick 3-Step Run (Copy & Paste)
cd /path/to/SoundBoardApp/dist
chmod +x LinuxSoundBoard
chmod +x ../assets/herbert_play.sh
./LinuxSoundBoard
