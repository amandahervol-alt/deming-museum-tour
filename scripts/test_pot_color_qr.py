import cv2
import numpy as np
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

TARGET_URL = "https://amandahervol-alt.github.io/deming-museum-tour/?room=7"
base_img_path = r"C:\Users\manet\.gemini\antigravity-ide\brain\6f34c999-2401-441a-aae3-0a0320e6d5be\.user_uploaded\media_1789917482175.jpg"
base_img = Image.open(base_img_path).convert("RGBA")
W, H = base_img.size

cx, cy = 382, 655

# Sample colors from the pot belly area (around x:350-410, y:630-680)
np_img = np.array(base_img)
pot_sample = np_img[630:680, 350:410, :3]
avg_pot_color = tuple(int(c) for c in np.mean(pot_sample, axis=(0, 1)))
print("Average pot background color (RGB):", avg_pot_color, "-> Hex:", "#{:02x}{:02x}{:02x}".format(*avg_pot_color))

# Also check median/lighter pot tone
light_pot_color = (205, 185, 145) # Warm sand/pot color
dark_red_brown = "#4A0F07"        # Very deep high-contrast Mimbres red-brown
mimbres_terracotta = "#6E170C"

detector = cv2.QRCodeDetector()

# Test 1: Direct transparent round-dot QR code placed straight on the pot (no white box at all!)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=2,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)

# Generate with CircleModuleDrawer on transparent background
img_circle_dots = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    color_mask=SolidFillColorMask(
        back_color=(avg_pot_color[0], avg_pot_color[1], avg_pot_color[2], 0), # transparent
        front_color=(74, 15, 7, 255) # Deep high contrast red-brown #4A0F07
    )
).convert("RGBA")

# Test sizes
for sz in [120, 130, 140, 150]:
    t1 = base_img.copy()
    res = img_circle_dots.resize((sz, sz), Image.Resampling.LANCZOS)
    t1.paste(res, (cx - sz//2, cy - sz//2), res)
    p = f"qr_codes/test_direct_pot_sz{sz}.jpg"
    t1.convert("RGB").save(p, quality=98)
    mat = cv2.imread(p)
    val, _, _ = detector.detectAndDecode(mat)
    print(f"Direct Pot Texture (sz={sz}): Scannable? -> {bool(val)} | Decoded: '{val}'")

# Test 2: Circular disc matching exact pot tone with dark red-brown round dots
for sz in [120, 130, 140]:
    r = int(sz * 0.72)
    t2 = base_img.copy()
    draw2 = ImageDraw.Draw(t2)
    # Circle matching pot color
    draw2.ellipse((cx - r, cy - r, cx + r, cy + r), fill=avg_pot_color + (255,))
    res = img_circle_dots.resize((sz, sz), Image.Resampling.LANCZOS)
    t2.paste(res, (cx - sz//2, cy - sz//2), res)
    p = f"qr_codes/test_pot_disc_sz{sz}.jpg"
    t2.convert("RGB").save(p, quality=98)
    mat = cv2.imread(p)
    val, _, _ = detector.detectAndDecode(mat)
    print(f"Pot Tone Disc (sz={sz}): Scannable? -> {bool(val)} | Decoded: '{val}'")

# Test 3: High contrast standard modules in dark red-brown (#3D0B05) directly on pot
img_std_pot = qr.make_image(fill_color="#3D0B05", back_color="#FFFFFF").convert("RGBA")
# Replace white with transparent
data = img_std_pot.getdata()
new_data = []
for item in data:
    if item[0] > 200 and item[1] > 200 and item[2] > 200:
        new_data.append((255, 255, 255, 0)) # transparent
    else:
        new_data.append((61, 11, 5, 255))
img_std_pot.putdata(new_data)

for sz in [120, 130, 140]:
    t3 = base_img.copy()
    res = img_std_pot.resize((sz, sz), Image.Resampling.LANCZOS)
    t3.paste(res, (cx - sz//2, cy - sz//2), res)
    p = f"qr_codes/test_std_transparent_pot_sz{sz}.jpg"
    t3.convert("RGB").save(p, quality=98)
    mat = cv2.imread(p)
    val, _, _ = detector.detectAndDecode(mat)
    print(f"Standard Transparent Direct on Pot (sz={sz}): Scannable? -> {bool(val)} | Decoded: '{val}'")
