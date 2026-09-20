import cv2
import numpy as np
from PIL import Image, ImageDraw
import qrcode
import os

TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=7"
base_img_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
base_img = Image.open(base_img_path).convert("RGBA")

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

# Var 3B: r=86 with 1.5px fine terracotta rim
var3B = base_img.copy()
draw3B = ImageDraw.Draw(var3B)
TERRACOTTA = (130, 25, 21, 255)
draw3B.ellipse((cx - r, cy - r, cx + r, cy + r), fill=TERRACOTTA)
draw3B.ellipse((cx - (r-2), cy - (r-2), cx + (r-2), cy + (r-2)), fill=(255, 255, 255, 255))
var3B.paste(qr_res, (cx - qr_size//2, cy - qr_size//2), qr_res)

out3B = "qr_codes/transportation_round_down_sz172_rim.jpg"
var3B.convert("RGB").save(out3B, quality=98)

# Check OpenCV detector
detector = cv2.QRCodeDetector()
mat3B = cv2.imread(out3B)
val3B, pts, _ = detector.detectAndDecode(mat3B)
print(f"Var 3B (r=86 with Terracotta Rim): Scannable? -> {bool(val3B)} | Decoded: '{val3B}'")

artifact_dir = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be"
var3B.convert("RGB").save(os.path.join(artifact_dir, "transportation_round_down_rim_sz172.jpg"), quality=98)
