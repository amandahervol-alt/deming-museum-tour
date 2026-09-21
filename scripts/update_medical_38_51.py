import os
import shutil
import json

src_audio = r"C:\Users\manet\Downloads\ElevenLabs_2026-09-21T01_38_51_Kirk Hunter - Friendly and Professional_pvc_sp115_s34_sb100_se87_b_m2.mp3"
dst_audio = "audio/room_8.mp3"

shutil.copy2(src_audio, dst_audio)
print(f"Copied {src_audio} -> {dst_audio} ({os.path.getsize(dst_audio)} bytes)")

# Backup repo
backup_dst = r"C:\Users\manet\.gemini\antigravity\scratch\deming-museum-ai-tour\audio\room_8.mp3"
if os.path.exists(os.path.dirname(backup_dst)):
    shutil.copy2(src_audio, backup_dst)
    print(f"Copied to backup repo: {backup_dst}")

transcript_text = (
    "This room may be difficult for some visitors, as it illustrates the medical practices and equipment in everyday use. "
    "The items were donated by the doctors and the hospitals that served Deming from the 1930s through the 1950s. "
    "Among the most striking pieces are two iron lungs — an adult version and an infant/child — that were used during the polio epidemics of 1949 and 1952. "
    "The Women's Hospital donated them to the Deming Memorial Hospital and funds were raised by the Deming Rotary Club to purchase and then donate them to the Museum. "
    "You'll also find a wooden birth chair from Spain, along with artifacts from hospitals and clinics throughout the Deming area, including the Women's Hospital, "
    "Faywood Hot Springs, the Camp Cody Red Cross Building and Infirmary, and Holy Cross Hospital, which operated for many years as a tuberculosis sanitarium. "
    "The nun doll on display was donated by the Holy Cross Order of South Bend, Indiana, along with a research paper detailing the order's history establishing and "
    "running the Holy Cross Sanitarium in Deming. Medicine has come a long way since these tools were in daily use."
)

# Update rooms.json
with open("data/rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)

for r in rooms:
    if r["id"] == 8:
        r["title"] = "Medical Room"
        r["subtitle"] = "Historic Healthcare, 1940s/50s Iron Lungs & Deming Sanitaria"
        r["audio"] = "audio/room_8.mp3"
        r["duration"] = "1:05"
        r["transcript"] = transcript_text
        r["highlights"] = [
            "1949 & 1952 Polio Epidemic Adult & Infant Iron Lungs",
            "Deming Rotary Club & Women's Hospital Donations",
            "Antique Spanish Wooden Birthing Chair",
            "Camp Cody Red Cross Infirmary & Faywood Hot Springs",
            "Holy Cross Tuberculosis Sanitarium & Sister Doll"
        ]
        print("Updated Room 8 in rooms.json")

with open("data/rooms.json", "w", encoding="utf-8") as f:
    json.dump(rooms, f, indent=2, ensure_ascii=False)

# Update museum_knowledge.json
with open("data/museum_knowledge.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

knowledge["key_collections"]["medical_room"] = {
    "era": "1930s to 1950s healthcare in Luna County & Southwest New Mexico",
    "iron_lungs": "Adult and infant/child iron lungs used during 1949 and 1952 polio epidemics, donated by Women's Hospital to Deming Memorial Hospital, with funds raised by Deming Rotary Club to purchase and donate them to the museum.",
    "birthing_chair": "Antique wooden birth chair imported from Spain.",
    "hospitals_represented": "Women's Hospital, Deming Memorial Hospital, Ladies Hospital, Faywood Hot Springs, Camp Cody Red Cross Building & Infirmary, and Holy Cross Hospital (tuberculosis sanitarium).",
    "holy_cross_sanitarium": "Nun doll and historical research paper donated by the Holy Cross Order of South Bend, Indiana, documenting their establishment of the sanitarium in Deming.",
    "narrator": "Kirk Hunter"
}

with open("data/museum_knowledge.json", "w", encoding="utf-8") as f:
    json.dump(knowledge, f, indent=2, ensure_ascii=False)

print("Updated data files successfully.")
