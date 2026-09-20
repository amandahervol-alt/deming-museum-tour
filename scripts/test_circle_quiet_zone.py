import cv2
import numpy as np
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=7"
base_img_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
base_img = Image.open(base_img_path).convert("RGBA")
W, H = base_img.size

# Let's test moving cy down a bit: cy = 655
cx = 382
cy = 655

detector = cv2.QRCodeDetector()

# Generate QR code with Level H and border=3
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=3, # generous quiet zone so circle mask doesn't clip finder eyes
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

img_qr = qr.make_image(fill_color="#821915", back_color="#FFFFFF").convert("RGBA")

# Let's test circular masking with different sizes and padding
for qr_size in [120, 130, 140, 150, 160]:
    resized = img_qr.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    
    # Create circular mask of size qr_size
    mask = Image.new("L", (qr_size, qr_size), 0)
    d_mask = ImageDraw.Draw(mask)
    d_mask.ellipse((0, 0, qr_size, qr_size), fill=255)
    
    # Circular QR
    round_qr = Image.new("RGBA", (qr_size, qr_size), (0, 0, 0, 0))
    round_qr.paste(resized, (0, 0), mask)
    
    test_img = base_img.copy()
    test_img.paste(round_qr, (cx - qr_size//2, cy - qr_size//2), round_qr)
    
    out_path = f"qr_codes/test_border3_sz{qr_size}.jpg"
    test_img.convert("RGB").save(out_path, quality=98)
    
    mat = cv2.imread(out_path)
    val, pts, _ = detector.detectAndDecode(mat)
    print(f"border=3, size={qr_size}: Scannable? -> {bool(val)} | Decoded: '{val}'")
