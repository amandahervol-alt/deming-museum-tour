import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import qrcode
import json

# 1. Ingest audio 28_20 into audio/room_13.mp3
src_audio = r"C:\Users\manet\Downloads\ElevenLabs_2026-09-21T01_28_20_Kirk Hunter - Friendly and Professional_pvc_sp115_s34_sb100_se87_b_m2.mp3"
dst_audio = "audio/room_13.mp3"

shutil.copy2(src_audio, dst_audio)
print(f"Copied {src_audio} -> {dst_audio} ({os.path.getsize(dst_audio)} bytes)")

# Backup repo
backup_dst = r"C:\Users\manet\.gemini\antigravity\scratch\deming-museum-ai-tour\audio\room_13.mp3"
if os.path.exists(os.path.dirname(backup_dst)):
    shutil.copy2(src_audio, backup_dst)
    print(f"Copied to backup repo: {backup_dst}")

# 2. Update rooms.json
transcript_text = (
    "The Hispanic Room is one of the most quietly powerful spaces in this museum. "
    "To understand why this room exists, you must understand something about this land. "
    "Long before Deming was a railroad town — long before the silver spike was driven here in 1881 connecting the southern transcontinental railroad, this was Mexico. "
    "Luna County, this valley, these streets we walk today, were once part of a Spanish and then Mexican world. That history didn't disappear when the borders shifted. "
    "It stayed woven into the daily life of this community — in the language spoken in homes, in the food on the table, in the faith carried from one generation to the next. "
    "That's what you'll find preserved here. "
    "This room holds the everyday textures of that Hispanic heritage — the objects, images, and traditions that tell the story of the families who built and sustained this region long before it ever appeared on a railroad map. "
    "It's a reminder that Deming's identity was never singular. It was shaped by Mimbres potters a thousand years ago, by Apache and Spanish soldiers at Fort Cummings, by railroad workers from a dozen different backgrounds and running through all of it, a deep and enduring Hispanic presence that predates the town itself. "
    "There's a small, almost playful detail in this room that captures something bigger: an old sign reading 'Hot Tamales — 10 cents.' It's a simple thing. But it's also a doorway. "
    "It reminds us that history isn't only found in treaties and railroad ledgers — it's found on street corners, in kitchens, in the small commerce of ordinary life. That sign could have hung outside a home in this very neighborhood, sold by a family whose descendants may still live in Luna County today. "
    "The Hispanic community is proud of its heritage. Nacio Herb Brown was born in Deming. He was a composer of songs, movie scores and Broadway theatre from the 1920s through the early 1950s. "
    "Some of his popular compositions you may recognize are: Singin' in the Rain, Temptation, and music from the Hopalong Cassidy TV series. The community stepped up to name a park after him. "
    "So, as you walk through this room, ask yourself to think of it not as a static exhibit, but as a living thread — one that connects the Mexico this land once was, to the Deming it became, to the community we stand in today. "
    "The pottery, the artifacts, the photographs — they're not just relics. They're proof that this heritage never left. It simply became part of the foundation everything else was built on."
)

with open("data/rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)

for r in rooms:
    if r["id"] == 13:
        r["title"] = "Hispanic Room"
        r["subtitle"] = "Deep-Rooted Heritage, Southwest History & Nacio Herb Brown"
        r["audio"] = "audio/room_13.mp3"
        r["duration"] = "2:29"
        r["transcript"] = transcript_text
        r["highlights"] = [
            "Pre-1881 Spanish & Mexican Borderlands Heritage",
            "Everyday Cultural Artifacts & Historic 10¢ Hot Tamales Sign",
            "Nacio Herb Brown (Composer of 'Singin' in the Rain' Born in Deming)",
            "Fort Cummings, Apache & Transcontinental Crossroads",
            "Living Cultural Traditions & Enduring Community Legacy"
        ]
        print("Updated Room 13 in rooms.json")

with open("data/rooms.json", "w", encoding="utf-8") as f:
    json.dump(rooms, f, indent=2, ensure_ascii=False)

# Update museum_knowledge.json
with open("data/museum_knowledge.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

knowledge["key_collections"]["hispanic_room"] = {
    "history": "Preserves the deep-rooted Hispanic, Spanish, and Mexican heritage that predates Deming's 1881 founding.",
    "hot_tamales_sign": "Historic 'Hot Tamales — 10 cents' sign representing everyday commerce, family traditions, and culinary heritage.",
    "nacio_herb_brown": "Famed American songwriter and Broadway/film composer born in Deming (wrote 'Singin' in the Rain', 'Temptation', Hopalong Cassidy score); local park named in his honor.",
    "cultural_continuity": "Highlights the enduring faith, language, customs, and community contributions across generations in Luna County.",
    "narrator": "Kirk Hunter"
}

with open("data/museum_knowledge.json", "w", encoding="utf-8") as f:
    json.dump(knowledge, f, indent=2, ensure_ascii=False)

# 3. Generate Poster for Hispanic Room (Room 13)
TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=13"

template_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
cv_img = cv2.imread(template_path)
H, W, _ = cv_img.shape

# Inpaint title box (y: 195 to 345, x: 90 to 674)
mask = np.zeros((H, W), dtype=np.uint8)
mask[195:345, 90:674] = 255
inpainted = cv2.inpaint(cv_img, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)

result = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGBA))
draw = ImageDraw.Draw(result)

# White lettering with dark drop shadow
font_title1 = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 42)
font_title2 = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 46)

title_line1 = "HISPANIC"
title_line2 = "ROOM"

def get_text_center(text, font, y_center):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (W - tw) / 2
    y = y_center - (th / 2)
    return x, y

x1, y1 = get_text_center(title_line1, font_title1, 235)
x2, y2 = get_text_center(title_line2, font_title2, 288)

shadow_color = (25, 18, 15, 230)
white_color = (255, 255, 255, 255)

# Drop shadow
for ox, oy in [(2, 2), (1, 2), (2, 1), (1, 1)]:
    draw.text((x1 + ox, y1 + oy), title_line1, font=font_title1, fill=shadow_color)
    draw.text((x2 + ox, y2 + oy), title_line2, font=font_title2, fill=shadow_color)

# Pure white text
draw.text((x1, y1), title_line1, font=font_title1, fill=white_color)
draw.text((x2, y2), title_line2, font=font_title2, fill=white_color)

# Generate Room 13 QR code in center between birds (cx=382, cy=655)
cx = 382
cy = 655
r = 86
qr_size = 120

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=2,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

img_qr = qr.make_image(fill_color="#821915", back_color="#FFFFFF").convert("RGBA")
qr_res = img_qr.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

# White round medallion with fine terracotta rim
TERRACOTTA = (130, 25, 21, 255)
draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=TERRACOTTA)
draw.ellipse((cx - (r-2), cy - (r-2), cx + (r-2), cy + (r-2)), fill=(255, 255, 255, 255))
result.paste(qr_res, (cx - qr_size//2, cy - qr_size//2), qr_res)

# Save poster files
out_jpg = "qr_codes/hispanic_room_poster_placard.jpg"
out_png = "qr_codes/hispanic_room_poster_placard.png"
rgb_result = result.convert("RGB")
rgb_result.save(out_jpg, quality=98)
result.save(out_png)

# Save artifact
artifact_dir = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be"
artifact_jpg = os.path.join(artifact_dir, "hispanic_room_poster_placard.jpg")
rgb_result.save(artifact_jpg, quality=98)

# Backup repo
backup_dir = r"C:\Users\manet\.gemini\antigravity\scratch\deming-museum-ai-tour\qr_codes"
if os.path.exists(backup_dir):
    rgb_result.save(os.path.join(backup_dir, "hispanic_room_poster_placard.jpg"), quality=98)

# Verify OpenCV scannability
detector = cv2.QRCodeDetector()
mat = cv2.imread(out_jpg)
val, pts, _ = detector.detectAndDecode(mat)
print(f"Hispanic Room Poster: Scannable? -> {bool(val)} | Decoded: '{val}'")
