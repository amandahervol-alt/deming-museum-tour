import cv2
import numpy as np
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, SquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=7"
base_img_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
base_img = Image.open(base_img_path).convert("RGBA")
W, H = base_img.size

# Let's test moving cy down: cy = 650, 655, 660
cx = 382
TERRACOTTA = (130, 25, 21, 255) # #821915

# Let's test QR with Error Correction H (30% redundancy)
# With Level H, we can clip the outer corners into a circle
qr = qrcode.QRCode(
    version=2, # slightly more modules so circle clipping leaves eyes intact
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=1,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

detector = cv2.QRCodeDetector()

for cy in [650, 655, 660]:
    for qr_size in [140, 150, 160]:
        # Generate base QR
        img_qr = qr.make_image(fill_color="#821915", back_color="#FFFFFF").convert("RGBA")
        img_qr = img_qr.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        # Make a circular mask
        mask = Image.new("L", (qr_size, qr_size), 0)
        d_mask = ImageDraw.Draw(mask)
        d_mask.ellipse((0, 0, qr_size, qr_size), fill=255)
        
        # Apply circular mask directly to QR image
        # This makes the QR code ITSELF round!
        round_qr = Image.new("RGBA", (qr_size, qr_size), (0, 0, 0, 0))
        round_qr.paste(img_qr, (0, 0), mask)
        
        # Paste onto base image at (cx, cy)
        test_img = base_img.copy()
        test_img.paste(round_qr, (cx - qr_size//2, cy - qr_size//2), round_qr)
        
        out_path = f"qr_codes/test_round_cy{cy}_sz{qr_size}.jpg"
        test_img.convert("RGB").save(out_path, quality=98)
        
        mat = cv2.imread(out_path)
        val, pts, _ = detector.detectAndDecode(mat)
        print(f"cy={cy}, size={qr_size}: Scannable? -> {bool(val)} | Decoded: '{val}'")
