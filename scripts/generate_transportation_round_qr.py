import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=7"
base_img_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
base_img = Image.open(base_img_path).convert("RGBA")
W, H = base_img.size

# Exact center between birds and under 'Deming Museum'
cx = 382
cy = 636

# Generate high-res QR code
# Using border=2 and error correction H (30% recovery)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=2,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

# Reddish-brown color matching Mimbres pottery red/terracotta: #821915
TERRACOTTA = (130, 25, 21, 255)       # #821915
WARM_CREAM = (255, 253, 248, 255)     # Very clean soft warm white

# --- Option A: Clean Round White Disc with Terracotta QR (Diameter 170px, Radius 85px) ---
optA = base_img.copy()
drawA = ImageDraw.Draw(optA)
rA = 85
qr_sizeA = 120 # Fits with plenty of quiet zone inside radius 85 (diagonal is 120*sqrt(2)/2 = 84.85)

# Draw crisp white round disc
drawA.ellipse((cx - rA, cy - rA, cx + rA, cy + rA), fill=(255, 255, 255, 255))

img_qrA = qr.make_image(fill_color="#821915", back_color="#FFFFFF").convert("RGBA")
img_qrA_res = img_qrA.resize((qr_sizeA, qr_sizeA), Image.Resampling.LANCZOS)
optA.paste(img_qrA_res, (cx - qr_sizeA//2, cy - qr_sizeA//2), img_qrA_res)

outA = "qr_codes/transportation_annex_round_qr_optionA.jpg"
optA.convert("RGB").save(outA, quality=98)

# --- Option B: Round Disc with Subtle Terracotta Accent Ring (Radius 88px) ---
optB = base_img.copy()
drawB = ImageDraw.Draw(optB)
rB = 88
# Thin outer terracotta ring
drawB.ellipse((cx - rB, cy - rB, cx + rB, cy + rB), fill=TERRACOTTA)
# Inner white circle
drawB.ellipse((cx - (rB-2), cy - (rB-2), cx + (rB-2), cy + (rB-2)), fill=(255, 255, 255, 255))

optB.paste(img_qrA_res, (cx - qr_sizeA//2, cy - qr_sizeA//2), img_qrA_res)

outB = "qr_codes/transportation_annex_round_qr_optionB.jpg"
optB.convert("RGB").save(outB, quality=98)

# --- Option C: Rounded-Modules QR in Round Disc (Smooth aesthetic) ---
optC = base_img.copy()
drawC = ImageDraw.Draw(optC)
rC = 86
drawC.ellipse((cx - rC, cy - rC, cx + rC, cy + rC), fill=(255, 255, 255, 255))

# Generate with RoundedModuleDrawer
img_qr_rounded = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=SolidFillColorMask(
        back_color=(255, 255, 255, 255),
        front_color=TERRACOTTA
    )
).convert("RGBA").resize((qr_sizeA, qr_sizeA), Image.Resampling.LANCZOS)

optC.paste(img_qr_rounded, (cx - qr_sizeA//2, cy - qr_sizeA//2), img_qr_rounded)

outC = "qr_codes/transportation_annex_round_qr_optionC.jpg"
optC.convert("RGB").save(outC, quality=98)

# Test scannability with OpenCV
detector = cv2.QRCodeDetector()
for name, p in [("Option A (Clean Round Disc)", outA), ("Option B (Round Disc + Ring)", outB), ("Option C (Rounded Modules Disc)", outC)]:
    mat = cv2.imread(p)
    val, pts, _ = detector.detectAndDecode(mat)
    print(f"{name}: Scannable? -> {bool(val)} | Decoded: '{val}'")
