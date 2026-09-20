import json, os, glob

with open('data/rooms.json', 'r', encoding='utf-8') as f:
    rooms = json.load(f)

print("CURRENT ROOMS IN ROOMS.JSON:")
for r in rooms:
    rid = r['id']
    title = r['title']
    audio = r.get('audio', 'none')
    print(f"  Room {rid:2}: {title:45} | audio: {audio}")

print("\nAUDIO FILES IN REPO:")
for f in sorted(glob.glob('audio/*.mp3')):
    print(f"  {f:20} -> {os.path.getsize(f)} bytes")
