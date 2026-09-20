import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
import json

# 1. Ingest audio 54_42 into audio/room_5.mp3
src_audio = r"C:\Users\manet\Downloads\ElevenLabs_2026-09-20T15_54_42_Kirk Hunter - Friendly and Professional_pvc_sp115_s34_sb100_se100_b_m2.mp3"
dst_audio = "audio/room_5.mp3"

shutil.copy2(src_audio, dst_audio)
print(f"Copied {src_audio} -> {dst_audio} ({os.path.getsize(dst_audio)} bytes)")

# Backup repo
backup_dst = r"C:\Users\manet\.gemini\antigravity\scratch\deming-museum-ai-tour\audio\room_5.mp3"
if os.path.exists(os.path.dirname(backup_dst)):
    shutil.copy2(src_audio, backup_dst)
    print(f"Copied to backup repo: {backup_dst}")

# 2. Update duration in rooms.json
with open("data/rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)

for r in rooms:
    if r["id"] == 5:
        r["audio"] = "audio/room_5.mp3"
        r["duration"] = "2:00"
        print("Updated Room 5 in rooms.json")

with open("data/rooms.json", "w", encoding="utf-8") as f:
    json.dump(rooms, f, indent=2, ensure_ascii=False)

# 3. Generate QR code for Room 5 (Bataan Death March)
TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=5"

# Base template from clean pot
template_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
cv_img = cv2.imread(template_path)
H, W, _ = cv_img.shape

# Inpaint title box (y: 195 to 345, x: 90 to 674)
mask = np.zeros((H, W), dtype=np.uint8)
mask[195:345, 90:674] = 255
inpainted = cv2.inpaint(cv_img, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)

result = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGBA))
draw = ImageDraw.Draw(result)

# Draw 'BATAAN DEATH MARCH DISPLAY' matching font styling
from PIL import ImageFont
font_title1 = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 36)
font_title2 = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 40)

title_line1 = "BATAAN DEATH MARCH"
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

# Drop shadow
shadow_color = (74, 16, 5, 200)
main_color = (130, 25, 21, 255)

for offset_x, offset_y in [(2, 2), (1, 1)]:
    draw.text((x1 + offset_x, y1 + offset_y), title_line1, font=font_title1, fill=shadow_color)
    draw.text((x2 + offset_x, y2 + offset_y), title_line2, font=font_title2, fill=shadow_color)

draw.text((x1, y1), title_line1, font=font_title1, fill=main_color)
draw.text((x2, y2), title_line2, font=font_title2, fill=main_color)

# Generate Room 5 QR code with CircleModuleDrawer (Round dots)
cx = 382
cy = 655
sz = 140

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=2,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

DARK_RED_BROWN = (65, 12, 6, 255) # #410C06

img_dots_transparent = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    color_mask=SolidFillColorMask(
        back_color=(0, 0, 0, 0),
        front_color=DARK_RED_BROWN
    )
).convert("RGBA").resize((sz, sz), Image.Resampling.LANCZOS)

# Direct pot blend poster
poster_direct = result.copy()
poster_direct.paste(img_dots_transparent, (cx - sz//2, cy - sz//2), img_dots_transparent)

out_jpg = "qr_codes/bataan_death_march_poster_placard.jpg"
out_png = "qr_codes/bataan_death_march_poster_placard.png"
poster_direct.convert("RGB").save(out_jpg, quality=98)
poster_direct.save(out_png)

# Also save clean round medallion version
poster_medallion = result.copy()
draw_med = ImageDraw.Draw(poster_medallion)
r = 85
qr_size = 120
draw_med.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255))
img_std = qr.make_image(fill_color="#821915", back_color="#FFFFFF").convert("RGBA").resize((qr_size, qr_size), Image.Resampling.LANCZOS)
poster_medallion.paste(img_std, (cx - qr_size//2, cy - qr_size//2), img_std)
out_med_jpg = "qr_codes/bataan_death_march_poster_medallion.jpg"
poster_medallion.convert("RGB").save(out_med_jpg, quality=98)

# Save artifacts
artifact_dir = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be"
poster_direct.convert("RGB").save(os.path.join(artifact_dir, "bataan_death_march_poster_direct.jpg"), quality=98)
poster_medallion.convert("RGB").save(os.path.join(artifact_dir, "bataan_death_march_poster_medallion.jpg"), quality=98)

# Verify OpenCV detector
detector = cv2.QRCodeDetector()
for name, p in [("Bataan Direct", out_jpg), ("Bataan Medallion", out_med_jpg)]:
    mat = cv2.imread(p)
    val, pts, _ = detector.detectAndDecode(mat)
    print(f"{name}: Scannable? -> {bool(val)} | Decoded: '{val}'")
