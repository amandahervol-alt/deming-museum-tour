import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=7"
base_img_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
base_img = Image.open(base_img_path).convert("RGBA")
W, H = base_img.size

# Placed down a bit in the widest center belly of the pot
cx = 382
cy = 655  # Moved down from 636 -> 655 (down by ~19px)

TERRACOTTA = (130, 25, 21, 255) # #821915

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=2,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

# Generate styled images
# 1. Standard QR with Reddish Brown #821915 on pure white
img_qr_std = qr.make_image(fill_color="#821915", back_color="#FFFFFF").convert("RGBA")

# Let's test a few variations of the round QR code at cy=655:

# --- Variation 1: Clean Round White Disc (Diameter 160px, Radius 80px, QR size 114px) ---
var1 = base_img.copy()
draw1 = ImageDraw.Draw(var1)
r1 = 80
qr_sz1 = 114
draw1.ellipse((cx - r1, cy - r1, cx + r1, cy + r1), fill=(255, 255, 255, 255))
qr_res1 = img_qr_std.resize((qr_sz1, qr_sz1), Image.Resampling.LANCZOS)
var1.paste(qr_res1, (cx - qr_sz1//2, cy - qr_sz1//2), qr_res1)
out1 = "qr_codes/transportation_round_down_clean.jpg"
var1.convert("RGB").save(out1, quality=98)

# --- Variation 2: Round Disc with Terracotta Rim Border (Diameter 164px, Radius 82px) ---
var2 = base_img.copy()
draw2 = ImageDraw.Draw(var2)
r2 = 82
draw2.ellipse((cx - r2, cy - r2, cx + r2, cy + r2), fill=TERRACOTTA)
draw2.ellipse((cx - (r2-2), cy - (r2-2), cx + (r2-2), cy + (r2-2)), fill=(255, 255, 255, 255))
qr_res2 = img_qr_std.resize((qr_sz1, qr_sz1), Image.Resampling.LANCZOS)
var2.paste(qr_res2, (cx - qr_sz1//2, cy - qr_sz1//2), qr_res2)
out2 = "qr_codes/transportation_round_down_rim.jpg"
var2.convert("RGB").save(out2, quality=98)

# --- Variation 3: Slightly Larger Round Disc (Diameter 170px, Radius 85px, QR size 120px) ---
var3 = base_img.copy()
draw3 = ImageDraw.Draw(var3)
r3 = 85
qr_sz3 = 120
draw3.ellipse((cx - r3, cy - r3, cx + r3, cy + r3), fill=(255, 255, 255, 255))
qr_res3 = img_qr_std.resize((qr_sz3, qr_sz3), Image.Resampling.LANCZOS)
var3.paste(qr_res3, (cx - qr_sz3//2, cy - qr_sz3//2), qr_res3)
out3 = "qr_codes/transportation_round_down_sz170.jpg"
var3.convert("RGB").save(out3, quality=98)

# --- Variation 4: Warm Ceramic Cream Round Disc (Radius 82px) ---
var4 = base_img.copy()
draw4 = ImageDraw.Draw(var4)
CERAMIC_CREAM = (248, 243, 233, 255)
draw4.ellipse((cx - r2, cy - r2, cx + r2, cy + r2), fill=CERAMIC_CREAM)
img_qr_ceramic = qr.make_image(fill_color="#70140A", back_color="#F8F3E9").convert("RGBA")
qr_res4 = img_qr_ceramic.resize((qr_sz1, qr_sz1), Image.Resampling.LANCZOS)
var4.paste(qr_res4, (cx - qr_sz1//2, cy - qr_sz1//2), qr_res4)
out4 = "qr_codes/transportation_round_down_ceramic.jpg"
var4.convert("RGB").save(out4, quality=98)

# Test OpenCV detection
detector = cv2.QRCodeDetector()
for name, p in [
    ("Var 1 (Clean r=80)", out1),
    ("Var 2 (Terracotta Rim r=82)", out2),
    ("Var 3 (Clean r=85)", out3),
    ("Var 4 (Ceramic Cream r=82)", out4),
]:
    mat = cv2.imread(p)
    val, pts, _ = detector.detectAndDecode(mat)
    print(f"{name}: Scannable? -> {bool(val)} | Decoded: '{val}'")

# Save primary artifact to brain folder
artifact_dir = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be"
var1.convert("RGB").save(os.path.join(artifact_dir, "transportation_round_down_clean.jpg"), quality=98)
var2.convert("RGB").save(os.path.join(artifact_dir, "transportation_round_down_rim.jpg"), quality=98)
var3.convert("RGB").save(os.path.join(artifact_dir, "transportation_round_down_sz170.jpg"), quality=98)
var4.convert("RGB").save(os.path.join(artifact_dir, "transportation_round_down_ceramic.jpg"), quality=98)
