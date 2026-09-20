#!/usr/bin/env python3
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import qrcode
import shutil

BASE_URL = "https://amandahervol-alt.github.io/deming-museum-tour"
ROOM_ID = 8
TARGET_URL = f"{BASE_URL}/?room={ROOM_ID}"

# 1. Base template
template_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789575966257.jpg"
if not os.path.exists(template_path):
    # Fallback to local copy
    template_path = "qr_codes/western_area_poster_placard.jpg"

cv_img = cv2.imread(template_path)
H, W, _ = cv_img.shape

# Inpaint title box (y: 195 to 345, x: 90 to 674)
mask = np.zeros((H, W), dtype=np.uint8)
mask[195:345, 90:674] = 255
inpainted = cv2.inpaint(cv_img, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)

result = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGBA))
draw = ImageDraw.Draw(result)

# 2. Draw 'MEDICAL ROOM'
font_title = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 44)
title_line1 = "MEDICAL"
title_line2 = "ROOM"

def get_text_center(text, font, y_center):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (W - tw) / 2
    y = y_center - (th / 2)
    return x, y

x1, y1 = get_text_center(title_line1, font_title, 235)
x2, y2 = get_text_center(title_line2, font_title, 290)

# Drop shadow
shadow_color = (74, 16, 5, 200)
main_color = (130, 25, 21, 255)

for offset_x, offset_y in [(2, 2), (1, 1)]:
    draw.text((x1 + offset_x, y1 + offset_y), title_line1, font=font_title, fill=shadow_color)
    draw.text((x2 + offset_x, y2 + offset_y), title_line2, font=font_title, fill=shadow_color)

draw.text((x1, y1), title_line1, font=font_title, fill=main_color)
draw.text((x2, y2), title_line2, font=font_title, fill=main_color)

# 3. Generate QR code for Room 8
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=1,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#821915", back_color="#FFFFFF").convert("RGBA")

# Center circle in the pot
cx, cy = 381, 657
r = 104

# Draw clean white circle
draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255))

# Resize QR and paste in center of the circle
qr_size = 144
qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
qx = cx - (qr_size // 2)
qy = cy - (qr_size // 2)

result.paste(qr_resized, (qx, qy), qr_resized)

# Save output
rgb_result = result.convert("RGB")
out_jpg = "qr_codes/medical_room_poster_placard.jpg"
out_png = "qr_codes/medical_room_poster_placard.png"
rgb_result.save(out_jpg, quality=98)
result.save(out_png)

# Save artifact
artifact_dir = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be"
artifact_jpg = os.path.join(artifact_dir, "medical_room_poster_placard.jpg")
rgb_result.save(artifact_jpg, quality=98)

print(f"Successfully generated {out_jpg} and {artifact_jpg}")
