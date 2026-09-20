import cv2
import numpy as np
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=7"
base_img_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
base_img = Image.open(base_img_path).convert("RGBA")
W, H = base_img.size

cx, cy = 382, 638

detector = cv2.QRCodeDetector()

# Let's test standard QR code with border=2, box_size=10
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=2,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

# Generate standard image with reddish-brown #821915 on white
img_std = qr.make_image(fill_color="#821915", back_color="#FFFFFF").convert("RGBA")

# Let's test different sizes: 130, 140, 150, 160
for qr_size in [130, 140, 150, 160]:
    r_disc = (qr_size // 2) + 2
    
    # 1. Circular white disc with square standard QR inside
    test = base_img.copy()
    draw = ImageDraw.Draw(test)
    draw.ellipse((cx - r_disc, cy - r_disc, cx + r_disc, cy + r_disc), fill=(255, 255, 255, 255))
    
    resized_qr = img_std.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    
    # Mask QR to circle so only circular region is pasted
    mask = Image.new("L", (qr_size, qr_size), 0)
    d_mask = ImageDraw.Draw(mask)
    d_mask.ellipse((0, 0, qr_size, qr_size), fill=255)
    
    test.paste(resized_qr, (cx - qr_size//2, cy - qr_size//2), mask)
    out_path = f"qr_codes/test_std_size_{qr_size}.jpg"
    test.convert("RGB").save(out_path, quality=98)
    
    mat = cv2.imread(out_path)
    val, pts, _ = detector.detectAndDecode(mat)
    print(f"Size {qr_size} (Circular Standard): Scannable? -> {bool(val)} | Decoded: '{val}'")

# Also test without circular clipping of the QR itself (square QR centered on circular white disc)
for qr_size in [120, 130, 140]:
    r_disc = int(qr_size * 0.72) # radius covers the square corners
    test = base_img.copy()
    draw = ImageDraw.Draw(test)
    # Circular white disc
    draw.ellipse((cx - r_disc, cy - r_disc, cx + r_disc, cy + r_disc), fill=(255, 255, 255, 255))
    resized_qr = img_std.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    test.paste(resized_qr, (cx - qr_size//2, cy - qr_size//2), resized_qr)
    out_path = f"qr_codes/test_disc_size_{qr_size}.jpg"
    test.convert("RGB").save(out_path, quality=98)
    
    mat = cv2.imread(out_path)
    val, pts, _ = detector.detectAndDecode(mat)
    print(f"Size {qr_size} (Square on Circular Disc r={r_disc}): Scannable? -> {bool(val)} | Decoded: '{val}'")
