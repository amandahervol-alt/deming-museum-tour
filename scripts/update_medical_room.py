import os
import shutil
import json

dl = r"C:\Users\manet\Downloads"

# 1. Copy Transportation audio (1:59) -> audio/room_7.mp3
transport_src = os.path.join(dl, "ElevenLabs_2026-09-19T15_01_55_Kirk Hunter - Friendly and Professional_pvc_sp115_s34_sb100_se100_b_m2.mp3")
if os.path.exists(transport_src):
    shutil.copy2(transport_src, "audio/room_7.mp3")
    print(f"Copied {transport_src} -> audio/room_7.mp3 ({os.path.getsize('audio/room_7.mp3')} bytes)")

# 2. Copy Medical Room audio (1:05) -> audio/room_8.mp3
medical_src = os.path.join(dl, "ElevenLabs_2026-09-19T15_06_57_Kirk Hunter - Friendly and Professional_pvc_sp115_s34_sb100_se100_b_m2.mp3")
if os.path.exists(medical_src):
    shutil.copy2(medical_src, "audio/room_8.mp3")
    print(f"Copied {medical_src} -> audio/room_8.mp3 ({os.path.getsize('audio/room_8.mp3')} bytes)")

# 3. Update rooms.json
with open("data/rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)

for r in rooms:
    if r["id"] == 7:
        r["duration"] = "1:59"
    elif r["id"] == 8:
        r["title"] = "Medical Room"
        r["subtitle"] = "Historic Healthcare, 1940s/50s Iron Lungs & Deming Sanitaria"
        r["audio"] = "audio/room_8.mp3"
        r["duration"] = "1:05"
        r["transcript"] = "This room may be difficult for some visitors, as it illustrates the medical practices and equipment once in everyday use. The items on display were donated by doctors and hospitals that served Deming from the 1930s through the 1950s. Among the most striking pieces are two iron lungs — an adult version and a child's — donated by the former Deming Memorial Hospital, where they were used during the polio epidemics of 1949 and 1952. The hospital contributed many other medical items on display here as well. You'll also find a wooden birthing chair from Spain, along with artifacts from hospitals and clinics throughout the Deming area, including the Ladies Hospital, Faywood Hot Springs, the Camp Cody Red Cross Building and Infirmary, and Holy Cross Hospital, which operated for many years as a tuberculosis sanitarium. The nun doll on display was donated by the Holy Cross Order of South Bend, Indiana, along with a research paper detailing the order's history establishing and running the Holy Cross Sanitarium in Deming. Medicine has come a long way since these tools were in daily use."
        r["highlights"] = [
            "1949 & 1952 Polio Epidemic Iron Lungs (Adult & Child)",
            "Deming Memorial Hospital 1930s–1950s Medical Artifacts",
            "Antique Spanish Wooden Birthing Chair",
            "Camp Cody Red Cross Infirmary & Faywood Hot Springs",
            "Holy Cross Tuberculosis Sanitarium & Sister Doll"
        ]

with open("data/rooms.json", "w", encoding="utf-8") as f:
    json.dump(rooms, f, indent=2, ensure_ascii=False)

print("Updated data/rooms.json successfully.")

# 4. Update museum_knowledge.json
with open("data/museum_knowledge.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

knowledge["key_collections"]["medical_room"] = {
    "era": "1930s to 1950s healthcare in Luna County & Southwest New Mexico",
    "iron_lungs": "Adult and child iron lungs donated by the former Deming Memorial Hospital, used during the 1949 and 1952 polio epidemics.",
    "birthing_chair": "Antique wooden birthing chair imported from Spain.",
    "hospitals_represented": "Deming Memorial Hospital, Ladies Hospital, Faywood Hot Springs, Camp Cody Red Cross Building & Infirmary, and Holy Cross Hospital (tuberculosis sanitarium).",
    "holy_cross_sanitarium": "Nun doll and historical research paper donated by the Holy Cross Order of South Bend, Indiana, documenting their establishment of the sanitarium in Deming.",
    "narrator": "Kirk Hunter"
}

with open("data/museum_knowledge.json", "w", encoding="utf-8") as f:
    json.dump(knowledge, f, indent=2, ensure_ascii=False)

print("Updated data/museum_knowledge.json successfully.")
