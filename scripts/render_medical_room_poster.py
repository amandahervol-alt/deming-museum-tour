import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import qrcode

# 1. Configuration
ROOM_ID = 8
TARGET_URL = f"https://amandahervol-alt.github.io/deming-museum-tour/?room={ROOM_ID}"

# 2. Template
template_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
cv_img = cv2.imread(template_path)
H, W, _ = cv_img.shape

# Inpaint title box (y: 195 to 345, x: 90 to 674)
mask = np.zeros((H, W), dtype=np.uint8)
mask[195:345, 90:674] = 255
inpainted = cv2.inpaint(cv_img, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)

result = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGBA))
draw = ImageDraw.Draw(result)

# 3. White Lettering with dark drop shadow (Same font, styling, and positioning as Transportation Annex)
font_title1 = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 42)
font_title2 = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 46)

title_line1 = "MEDICAL"
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

# 4. Generate Room 8 QR code in center between birds
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

# 5. Save poster files
out_jpg = "qr_codes/medical_room_poster_placard.jpg"
out_png = "qr_codes/medical_room_poster_placard.png"
rgb_result = result.convert("RGB")
rgb_result.save(out_jpg, quality=98)
result.save(out_png)

# Save artifact
artifact_dir = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be"
artifact_jpg = os.path.join(artifact_dir, "medical_room_poster_placard.jpg")
rgb_result.save(artifact_jpg, quality=98)

# Backup repo
backup_dir = r"C:\Users\manet\.gemini\antigravity\scratch\deming-museum-ai-tour\qr_codes"
if os.path.exists(backup_dir):
    rgb_result.save(os.path.join(backup_dir, "medical_room_poster_placard.jpg"), quality=98)

# Verify OpenCV scannability
detector = cv2.QRCodeDetector()
mat = cv2.imread(out_jpg)
val, pts, _ = detector.detectAndDecode(mat)
print(f"Medical Room Poster: Scannable? -> {bool(val)} | Decoded: '{val}'")
