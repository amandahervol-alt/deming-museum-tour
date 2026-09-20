import cv2
import numpy as np
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

# Target URL for Transportation Annex (Room 7)
TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=7"

# Load base image
base_img_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
base_img = Image.open(base_img_path).convert("RGBA")
W, H = base_img.size

# Let's test different center coordinates:
# Under 'Deming Museum' and between birds:
# cx = 382, cy = 638
cx, cy = 382, 638

# Test 1: Direct QR on pot with CircleModuleDrawer (Reddish brown #7E1E11)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=8,
    border=1,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

# Generate styled QR
img_circle_dots = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    color_mask=SolidFillColorMask(
        back_color=(255, 255, 255, 0), # transparent back
        front_color=(126, 30, 17, 255) # reddish brown
    )
).convert("RGBA")

# Also test with a circular mask on the QR code
qr_size = 150
img_circle_dots_resized = img_circle_dots.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

# Create a circular mask for round QR code
mask_circle = Image.new("L", (qr_size, qr_size), 0)
draw_mask = ImageDraw.Draw(mask_circle)
draw_mask.ellipse((0, 0, qr_size, qr_size), fill=255)

# Test variation 1: Transparent back directly on pot
test1 = base_img.copy()
test1.paste(img_circle_dots_resized, (cx - qr_size//2, cy - qr_size//2), img_circle_dots_resized)
test1.convert("RGB").save("qr_codes/test1_transparent_dots.jpg", quality=98)

# Test variation 2: Subtle warm ivory circular disc background (matching pot highlights)
test2 = base_img.copy()
draw2 = ImageDraw.Draw(test2)
r_disc = (qr_size // 2) + 4
# Warm ivory circle matching light pot tone
draw2.ellipse((cx - r_disc, cy - r_disc, cx + r_disc, cy + r_disc), fill=(255, 253, 248, 240))
# QR with front color reddish brown #821915
img_dots_solid = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    color_mask=SolidFillColorMask(
        back_color=(255, 253, 248, 0),
        front_color=(130, 25, 21, 255)
    )
).convert("RGBA").resize((qr_size, qr_size), Image.Resampling.LANCZOS)
test2.paste(img_dots_solid, (cx - qr_size//2, cy - qr_size//2), img_dots_solid)
test2.convert("RGB").save("qr_codes/test2_ivory_disc_dots.jpg", quality=98)

# Test variation 3: Crisp circular QR code with RoundedModuleDrawer and soft rim
test3 = base_img.copy()
draw3 = ImageDraw.Draw(test3)
# Draw circular background
draw3.ellipse((cx - r_disc, cy - r_disc, cx + r_disc, cy + r_disc), fill=(255, 255, 255, 255))
img_rounded = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=SolidFillColorMask(
        back_color=(255, 255, 255, 0),
        front_color=(130, 25, 21, 255)
    )
).convert("RGBA").resize((qr_size, qr_size), Image.Resampling.LANCZOS)
test3.paste(img_rounded, (cx - qr_size//2, cy - qr_size//2), img_rounded)
test3.convert("RGB").save("qr_codes/test3_rounded_modules.jpg", quality=98)

# Test scannability with OpenCV
detector = cv2.QRCodeDetector()
for name, fpath in [
    ("Test 1 (Transparent)", "qr_codes/test1_transparent_dots.jpg"),
    ("Test 2 (Ivory Disc)", "qr_codes/test2_ivory_disc_dots.jpg"),
    ("Test 3 (Rounded/White Disc)", "qr_codes/test3_rounded_modules.jpg")
]:
    mat = cv2.imread(fpath)
    val, pts, _ = detector.detectAndDecode(mat)
    print(f"{name}: Scannable? -> {bool(val)} (Decoded: '{val}')")
