#!/bin/bash
# ------------------- Debian Soundboard -------------------

# Stop all mpv instances
killall -q mpv
sleep 0.03

# Create Soundboard sink if missing
if ! pactl list short sinks | grep -q Soundboard ; then
    echo "[+] Soundboard missing → creating..."
    pactl load-module module-null-sink sink_name=Soundboard sink_properties=device.description=Soundboard
fi

# Create Heatsink sink if missing
if ! pactl list short sinks | grep -q Heatsink ; then
    echo "[+] Heatsink missing → creating..."
    pactl load-module module-null-sink sink_name=Heatsink sink_properties=device.description=Heatsink
fi

# Loopback Soundboard → Heatsink
if ! pactl list short modules | grep "Soundboard.monitor" | grep -q "sink=Heatsink" ; then
    echo "[+] Creating loopback Soundboard → Heatsink"
    pactl load-module module-loopback source=Soundboard.monitor sink=Heatsink latency_msec=20
fi

# Loopback Soundboard → Default Sink
DEFAULT_SINK=$(pactl get-default-sink)
if ! pactl list short modules | grep "Soundboard.monitor" | grep -q "$DEFAULT_SINK" ; then
    echo "[+] Creating loopback Soundboard → Default Sink"
    pactl load-module module-loopback source=Soundboard.monitor sink=$DEFAULT_SINK latency_msec=20
fi

# Heatsink volume
pactl set-sink-volume Heatsink 125%
pactl set-sink-mute Heatsink 0

# Play MP3
MP3_FILE="$1"
if [ -f "$MP3_FILE" ]; then
    mpv --audio-device=pulse/Soundboard --really-quiet --no-video "$MP3_FILE"
else
    echo "[!] File not found: $MP3_FILE"
fi
