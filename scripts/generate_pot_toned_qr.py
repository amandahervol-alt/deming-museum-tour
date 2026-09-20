import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
import os

TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=7"
base_img_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
base_img = Image.open(base_img_path).convert("RGBA")
W, H = base_img.size

cx = 382
cy = 655
sz = 140

# Generate styled QR code with CircleModuleDrawer (Round dots)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=2,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

# Deep high-contrast Mimbres reddish-brown for perfect scanning
DARK_RED_BROWN = (65, 12, 6, 255) # #410C06

img_dots_transparent = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    color_mask=SolidFillColorMask(
        back_color=(0, 0, 0, 0),
        front_color=DARK_RED_BROWN
    )
).convert("RGBA").resize((sz, sz), Image.Resampling.LANCZOS)

# -------------------------------------------------------------
# Option 1: Direct on Pot (100% transparent, pot texture fully shows through)
# -------------------------------------------------------------
opt1 = base_img.copy()
opt1.paste(img_dots_transparent, (cx - sz//2, cy - sz//2), img_dots_transparent)
out1 = "qr_codes/transportation_direct_pot_round_dots.jpg"
opt1.convert("RGB").save(out1, quality=98)

# -------------------------------------------------------------
# Option 2: Soft Feathered Circular Pot Tone (Gently brightened clay circle under round dots)
# -------------------------------------------------------------
opt2 = base_img.copy()
# Create a smooth feathered radial glow in the pot's warm clay color
halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_halo = ImageDraw.Draw(halo)
r_halo = 82
# Subtle warm pot highlight
draw_halo.ellipse((cx - r_halo, cy - r_halo, cx + r_halo, cy + r_halo), fill=(235, 218, 180, 140))
halo = halo.filter(ImageFilter.GaussianBlur(8))
opt2.paste(halo, (0, 0), halo)
opt2.paste(img_dots_transparent, (cx - sz//2, cy - sz//2), img_dots_transparent)
out2 = "qr_codes/transportation_soft_clay_halo_dots.jpg"
opt2.convert("RGB").save(out2, quality=98)

# -------------------------------------------------------------
# Option 3: Circular Pot Medallion with Fine Terracotta Ring
# -------------------------------------------------------------
opt3 = base_img.copy()
draw3 = ImageDraw.Draw(opt3)
r3 = 84
# Sampled pot clay color
POT_CLAY = (212, 192, 154, 255)
TERRACOTTA = (110, 23, 12, 255)
# Fine terracotta circle
draw3.ellipse((cx - r3, cy - r3, cx + r3, cy + r3), fill=TERRACOTTA)
# Filled with exact pot clay color
draw3.ellipse((cx - (r3-2), cy - (r3-2), cx + (r3-2), cy + (r3-2)), fill=POT_CLAY)
opt3.paste(img_dots_transparent, (cx - sz//2, cy - sz//2), img_dots_transparent)
out3 = "qr_codes/transportation_pot_clay_ring_dots.jpg"
opt3.convert("RGB").save(out3, quality=98)

# Test OpenCV detector on all 3
detector = cv2.QRCodeDetector()
for name, p in [
    ("Option 1 (Direct on Pot Texture)", out1),
    ("Option 2 (Soft Feathered Clay Tone)", out2),
    ("Option 3 (Clay Disc with Fine Terracotta Ring)", out3)
]:
    mat = cv2.imread(p)
    val, pts, _ = detector.detectAndDecode(mat)
    print(f"{name}: Scannable? -> {bool(val)} | Decoded: '{val}'")

# Save artifacts to brain folder
artifact_dir = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be"
opt1.convert("RGB").save(os.path.join(artifact_dir, "transportation_direct_pot_round_dots.jpg"), quality=98)
opt2.convert("RGB").save(os.path.join(artifact_dir, "transportation_soft_clay_halo_dots.jpg"), quality=98)
opt3.convert("RGB").save(os.path.join(artifact_dir, "transportation_pot_clay_ring_dots.jpg"), quality=98)
