import shutil
import os
import json

src = r"C:\Users\manet\Downloads\ElevenLabs_2026-09-20T15_54_42_Kirk Hunter - Friendly and Professional_pvc_sp115_s34_sb100_se100_b_m2.mp3"
dst = "audio/room_7.mp3"

shutil.copy2(src, dst)
print(f"Copied {src} -> {dst} ({os.path.getsize(dst)} bytes)")

backup_dst = r"C:\Users\manet\.gemini\antigravity\scratch\deming-museum-ai-tour\audio\room_7.mp3"
if os.path.exists(os.path.dirname(backup_dst)):
    shutil.copy2(src, backup_dst)
    print(f"Copied to backup repo: {backup_dst}")

# Check rooms.json
with open("data/rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)

for r in rooms:
    if r["id"] == 7:
        print(f"Room 7 Title: {r['title']}")
        print(f"Room 7 Audio: {r.get('audio')}")
        print(f"Room 7 Duration: {r.get('duration')}")
