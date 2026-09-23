import os
import re
import json
import docx

dl = r"C:\Users\manet\Downloads"

script_files = {
    1: "Old Timer's (1).docx",
    2: "Mimbres Indians & Pottery.docx",
    3: "History_of_Building.docx",
    4: "Military_Room_revised.docx",
    5: "Bataan_Death_March_revised.docx",
    6: "Doll and Toy Room.docx",
    7: "Transportation.docx",
    8: "Medical (1).docx",
    9: "Western Area.docx",
    10: "Quilt_Room_revised.docx",
    11: "Main Street.docx",
    12: "Geodes_revised.docx",
    13: "Hispanic Room (1).docx",
    14: "Czech (1).docx"
}

def clean_script_text(text):
    # Fix smart quotes and typographic characters
    text = text.replace("\u2018", "'").replace("\u2019", "'").replace("`", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2014", " — ").replace("\u2013", "–")
    text = text.replace("\ufffd", " — ")
    # Fix spacing around dashes and punctuation
    text = re.sub(r'\s*—\s*', ' — ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Load current rooms
with open("data/rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)

for r in rooms:
    rid = r["id"]
    if rid not in script_files:
        continue
    
    doc_path = os.path.join(dl, script_files[rid])
    if not os.path.exists(doc_path):
        print(f"[WARN] File not found for Room {rid}: {doc_path}")
        continue
    
    doc = docx.Document(doc_path)
    paras = [clean_script_text(p.text) for p in doc.paragraphs if p.text.strip()]
    
    # Filter out title-only header lines
    first = paras[0].lower()
    title_prefixes = [
        "old timer", "mimbres", "history of building", "military room",
        "bataan death march", "doll/toy", "doll and toy", "transportation",
        "medical", "western area", "quilt", "main street", "welcome to the geode",
        "hispanic room", "czechoslovakian"
    ]
    if any(first.startswith(tp) for tp in title_prefixes):
        body_paras = paras[1:]
    else:
        body_paras = paras
    
    # Remove citations at the very end if present (e.g. O.T. Snodgrass in Mimbres)
    cleaned_body = []
    for p in body_paras:
        if p.startswith("From REALISTIC") or p.startswith("By O.T. Snodgrass"):
            continue
        cleaned_body.append(p)
    
    full_transcript = " ".join(cleaned_body)
    
    # Specific targeted polish for typos in source docx files:
    full_transcript = re.sub(r'1881connecting', '1881 connecting', full_transcript)
    full_transcript = re.sub(r'1959 — 1960-time frame|1959–1960-time frame', '1959–1960 timeframe', full_transcript)
    full_transcript = re.sub(r'reigned on the daughter', 'rained on the daughter', full_transcript)
    full_transcript = re.sub(r'\bsolider\b', 'soldier', full_transcript)
    full_transcript = re.sub(r'adjourning Old Timers', 'adjoining Old Timers', full_transcript)
    full_transcript = re.sub(r'bult on', 'built on', full_transcript)
    full_transcript = re.sub(r'and old sign reading', 'an old sign reading', full_transcript)
    full_transcript = re.sub(r'Singing in the Rain', 'Singin\' in the Rain', full_transcript)
    full_transcript = re.sub(r'1930 — s through the 1950 — s|1930\s*–\s*s through the 1950\s*–\s*s', '1930s through the 1950s', full_transcript)
    full_transcript = re.sub(r'Camp Codey', 'Camp Cody', full_transcript)
    full_transcript = re.sub(r'Hatchita', 'Hachita', full_transcript)
    full_transcript = re.sub(r'a old casket', 'an old casket', full_transcript)
    full_transcript = re.sub(r'Deming Czechoslovakian community', "Deming's Czechoslovakian community", full_transcript)
    full_transcript = re.sub(r' — s\b', "'s", full_transcript)
    
    r["transcript"] = full_transcript
    print(f"[OK] Room {rid:02d}: {r['title']} -> {len(full_transcript)} characters")

# Save updated rooms.json
with open("data/rooms.json", "w", encoding="utf-8") as f:
    json.dump(rooms, f, indent=2, ensure_ascii=False)

print("\nSuccessfully updated all room scripts in data/rooms.json!")
