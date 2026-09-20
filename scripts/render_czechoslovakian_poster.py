import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
import json

# 1. Ingest audio 28_14 (ElevenLabs_2026-09-20T19_28_41...) into audio/room_14.mp3
src_audio = r"C:\Users\manet\Downloads\ElevenLabs_2026-09-20T19_28_41_Kirk Hunter - Friendly and Professional_pvc_sp115_s34_sb100_se87_b_m2.mp3"
dst_audio = "audio/room_14.mp3"

shutil.copy2(src_audio, dst_audio)
print(f"Copied {src_audio} -> {dst_audio} ({os.path.getsize(dst_audio)} bytes)")

# Backup repo
backup_dst = r"C:\Users\manet\.gemini\antigravity\scratch\deming-museum-ai-tour\audio\room_14.mp3"
if os.path.exists(os.path.dirname(backup_dst)):
    shutil.copy2(src_audio, backup_dst)
    print(f"Copied to backup repo: {backup_dst}")

# 2. Update rooms.json
with open("data/rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)

for r in rooms:
    if r["id"] == 14:
        r["title"] = "Czechoslovakian Display"
        r["subtitle"] = "1920s Heritage, Czech Farming & The Annual Klobase Festival"
        r["audio"] = "audio/room_14.mp3"
        r["duration"] = "1:28"
        r["transcript"] = "The history of Deming's Czechoslovakian community began in the 1920s. Czech immigrants were fleeing the civil war in their home country. Many were cotton farmers searching for rich farming land as they migrated to America, through Ellis Island and the ports of Galveston, Texas. Several Czech families settled in Deming and began farming. In the fall, the families would gather to celebrate the end of the harvest season by gathering and sharing their heritage foods, which included Klobase. In 1928, the Czech immigrants, who attended Holy Family Catholic church, organized a fundraiser and the first official Klobase Festival started. Traditional Czech food was served to the community under the trees at the Kostelnik Farm and the casings for the Klobase were brought in from Texas. As the event grew, more preparation space was needed and the space moved to the Knights of Columbus building which is now part of the Luna County Sheriff Office. Frankie and Kathy Hervol, who bought the Kostelnik Farm in 1972, donated the land and building back to the church so that the Klobase Festival would have a permanent preparation location to where it started in 1928. The festival is held on the third Sunday of October at Luna County Courthouse Park, serves approximately 2,500 people and the Old Timers group coordinates their yearly reunion with this festival. Today the descendants of the founders of this festival carry on the tradition of the recipes that have been passed down through the generations."
        r["highlights"] = [
            "1920s Czech Immigration via Ellis Island & Galveston",
            "Cotton Farming Pioneers of Luna County",
            "1928 First Klobase Festival & Kostelnik Farm",
            "Holy Family Church & Hervol Family Dedication",
            "Annual October Courthouse Park Festival (2,500+ Served)"
        ]
        print("Updated Room 14 in rooms.json")

with open("data/rooms.json", "w", encoding="utf-8") as f:
    json.dump(rooms, f, indent=2, ensure_ascii=False)

# Update museum_knowledge.json
with open("data/museum_knowledge.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

knowledge["key_collections"]["czechoslovakian_display"] = {
    "heritage": "1920s Czech immigration fleeing civil war, entering via Ellis Island and Galveston, TX to farm cotton in Deming.",
    "klobase_festival": "Started in 1928 as a fundraiser by Czech immigrants attending Holy Family Catholic Church, hosted under trees at Kostelnik Farm.",
    "kostelnik_hervol_farm": "Frankie & Kathy Hervol purchased the Kostelnik Farm in 1972 and donated land/building to church for permanent preparation.",
    "courthouse_park_tradition": "Held annually on 3rd Sunday of October at Luna County Courthouse Park, serving ~2,500 people alongside Old Timers Reunion.",
    "narrator": "Kirk Hunter"
}

with open("data/museum_knowledge.json", "w", encoding="utf-8") as f:
    json.dump(knowledge, f, indent=2, ensure_ascii=False)

# 3. Generate Poster for Czechoslovakian Display (Room 14)
TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=14"

template_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789932740469.jpg"
cv_img = cv2.imread(template_path)
H, W, _ = cv_img.shape

# Inpaint title box (y: 195 to 345, x: 90 to 674)
mask = np.zeros((H, W), dtype=np.uint8)
mask[195:345, 90:674] = 255
inpainted = cv2.inpaint(cv_img, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)

result = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGBA))
draw = ImageDraw.Draw(result)

# White lettering with dark drop shadow
font_title1 = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 36)
font_title2 = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 44)

title_line1 = "CZECHOSLOVAKIAN"
title_line2 = "DISPLAY"

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

# Generate Room 14 QR code in center between birds (cx=382, cy=655)
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
out_jpg = "qr_codes/czechoslovakian_display_poster_placard.jpg"
out_png = "qr_codes/czechoslovakian_display_poster_placard.png"
rgb_result = result.convert("RGB")
rgb_result.save(out_jpg, quality=98)
result.save(out_png)

# Save artifact
artifact_dir = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be"
artifact_jpg = os.path.join(artifact_dir, "czechoslovakian_display_poster_placard.jpg")
rgb_result.save(artifact_jpg, quality=98)

# Backup repo
backup_dir = r"C:\Users\manet\.gemini\antigravity\scratch\deming-museum-ai-tour\qr_codes"
if os.path.exists(backup_dir):
    rgb_result.save(os.path.join(backup_dir, "czechoslovakian_display_poster_placard.jpg"), quality=98)

# Verify OpenCV scannability
detector = cv2.QRCodeDetector()
mat = cv2.imread(out_jpg)
val, pts, _ = detector.detectAndDecode(mat)
print(f"Czechoslovakian Display Poster: Scannable? -> {bool(val)} | Decoded: '{val}'")
