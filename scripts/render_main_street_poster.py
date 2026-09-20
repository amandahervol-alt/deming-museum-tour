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

# 1. Ingest audio 09_21 into audio/room_11.mp3
src_audio = r"C:\Users\manet\Downloads\ElevenLabs_2026-09-20T18_09_21_Kirk Hunter - Friendly and Professional_pvc_sp115_s34_sb100_se87_b_m2.mp3"
dst_audio = "audio/room_11.mp3"

shutil.copy2(src_audio, dst_audio)
print(f"Copied {src_audio} -> {dst_audio} ({os.path.getsize(dst_audio)} bytes)")

# Backup repo
backup_dst = r"C:\Users\manet\.gemini\antigravity\scratch\deming-museum-ai-tour\audio\room_11.mp3"
if os.path.exists(os.path.dirname(backup_dst)):
    shutil.copy2(src_audio, backup_dst)
    print(f"Copied to backup repo: {backup_dst}")

# 2. Update rooms.json
with open("data/rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)

for r in rooms:
    if r["id"] == 11:
        r["title"] = "Main Street Display"
        r["subtitle"] = "Historic Storefronts, 1890s Hearse & The Deming Headlight"
        r["audio"] = "audio/room_11.mp3"
        r["duration"] = "1:25"
        r["transcript"] = "Upon this location's opening, the museum started to receive so many donations that it ran out of room and discussions were held to add additions. One such discussion was to recreate a storefront exhibit of Deming. What you see first are horse-drawn carriages: a hearse donated by Baca Funeral Home last used in the 90s; buggies used for going to church and courting; a sleigh, even though Deming only receives an average of nine inches of precipitation per year; and various wagons used by families, farmers, and ranchers. To the right of the hearse is Deming's first traffic light and an old gas pump. The recreated shops illustrate what items were available: Mahoney Hardware houses the washing machine that sparked the founding of this museum; alongside a dental office, beauty salon, dress shop, post office, livery stable, funeral parlor with an antique casket, and barber shop with original storefront signs. The Deming Headlight is of particular interest as the oldest continuously published newspaper in the state; look in the window to see an antique typewriter, an over-engineered pencil sharpener, and their original, massive vintage printing press."
        r["highlights"] = [
            "Baca Funeral Home 1890s Horse-Drawn Hearse & Sleigh",
            "Deming's First Working Traffic Light & Vintage Gas Pump",
            "Mahoney Hardware & The Museum-Founding Washing Machine",
            "Recreated Main Street Shops: Barber, Dentist, Millinery & Post Office",
            "The Deming Headlight Newspaper & Heavy Antique Printing Press"
        ]
        print("Updated Room 11 in rooms.json")

with open("data/rooms.json", "w", encoding="utf-8") as f:
    json.dump(rooms, f, indent=2, ensure_ascii=False)

# Update museum_knowledge.json
with open("data/museum_knowledge.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

knowledge["key_collections"]["main_street"] = {
    "storefronts": "Recreated vintage Deming Main Street with Mahoney Hardware, barber shop, dental clinic, millinery/dress shop, post office, beauty salon, livery stable, and funeral parlor.",
    "hearse_and_vehicles": "Horse-drawn hearse from Baca Funeral Home (last used in the 1890s/1900s), courting buggies, snow sleigh, farm wagons.",
    "mahoney_hardware": "Features the historic washing machine donation that originally sparked the founding of the museum.",
    "deming_headlight": "Oldest continuously published newspaper in New Mexico; original heavy antique printing press and vintage office equipment on display.",
    "narrator": "Kirk Hunter"
}

with open("data/museum_knowledge.json", "w", encoding="utf-8") as f:
    json.dump(knowledge, f, indent=2, ensure_ascii=False)

# 3. Generate Poster for Main Street Display (Room 11)
TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=11"

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
font_title1 = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 40)
font_title2 = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 44)

title_line1 = "MAIN STREET"
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

# Generate Room 11 QR code
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
out_jpg = "qr_codes/main_street_display_poster_placard.jpg"
out_png = "qr_codes/main_street_display_poster_placard.png"
rgb_result = result.convert("RGB")
rgb_result.save(out_jpg, quality=98)
result.save(out_png)

# Save artifact
artifact_dir = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be"
artifact_jpg = os.path.join(artifact_dir, "main_street_display_poster_placard.jpg")
rgb_result.save(artifact_jpg, quality=98)

# Backup repo
backup_dir = r"C:\Users\manet\.gemini\antigravity\scratch\deming-museum-ai-tour\qr_codes"
if os.path.exists(backup_dir):
    rgb_result.save(os.path.join(backup_dir, "main_street_display_poster_placard.jpg"), quality=98)

# Verify OpenCV scannability
detector = cv2.QRCodeDetector()
mat = cv2.imread(out_jpg)
val, pts, _ = detector.detectAndDecode(mat)
print(f"Main Street Display Poster: Scannable? -> {bool(val)} | Decoded: '{val}'")
