import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
import qrcode

TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=7"
base_img_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
base_img = Image.open(base_img_path).convert("RGBA")
W, H = base_img.size

cx = 382
cy = 636

# Generate high-res QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=2,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

# Test Option D: Cream tone disc matching pot ceramic (#F5EFE0) with deep reddish brown (#7A180E)
CERAMIC_CREAM = (248, 243, 233, 255) # #F8F3E9
DEEP_RED_BROWN = "#70140A"

img_qrD = qr.make_image(fill_color=DEEP_RED_BROWN, back_color="#F8F3E9").convert("RGBA")
qr_size = 120
r = 85

optD = base_img.copy()
drawD = ImageDraw.Draw(optD)
drawD.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CERAMIC_CREAM)
img_qrD_res = img_qrD.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
optD.paste(img_qrD_res, (cx - qr_size//2, cy - qr_size//2), img_qrD_res)

outD = "qr_codes/transportation_annex_round_qr_optionD.jpg"
optD.convert("RGB").save(outD, quality=98)

# Save best version as primary artifact
artifact_dir = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be"
optA = Image.open("qr_codes/transportation_annex_round_qr_optionA.jpg")
optA.save(os.path.join(artifact_dir, "transportation_annex_round_qr.jpg"), quality=98)
optB = Image.open("qr_codes/transportation_annex_round_qr_optionB.jpg")
optB.save(os.path.join(artifact_dir, "transportation_annex_round_qr_ring.jpg"), quality=98)
optD.convert("RGB").save(os.path.join(artifact_dir, "transportation_annex_round_qr_ceramic.jpg"), quality=98)

# Test scannability
detector = cv2.QRCodeDetector()
matD = cv2.imread(outD)
valD, pts, _ = detector.detectAndDecode(matD)
print(f"Option D (Ceramic Cream Disc): Scannable? -> {bool(valD)} | Decoded: '{valD}'")
