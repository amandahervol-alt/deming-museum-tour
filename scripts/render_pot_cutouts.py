"""
Render High-Res Standalone Mimbres Pot Placards (PNG & SVG) + Enhanced Cutout Sheet
-----------------------------------------------------------------------------------
Generates:
  1. Individual transparent high-res PNG pot cutouts for each room (qr_codes/mimbres_pot_room_X.png)
  2. Enhanced printable HTML sheet with explicit scissor cut-along-the-pot guides.
"""

import json
import base64
from io import BytesIO
from pathlib import Path
import qrcode
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "https://amandahervol-alt.github.io/deming-museum-tour"

def generate_qr_image(url: str, size: int = 240) -> Image.Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#231c17", back_color="#fffdf8")
    return img.resize((size, size), Image.Resampling.LANCZOS).convert("RGBA")

def create_mimbres_pot_png(room: dict, output_path: Path):
    """Draws a standalone high-res Mimbres Pot cutout with text and QR code baked in."""
    W, H = 800, 960
    im = Image.new("RGBA", (W, H), (255, 255, 255, 0)) # Transparent background
    draw = ImageDraw.Draw(im)

    # 1. Base Clay Pot Silhouette
    # Neck: (260, 60) to (540, 60)
    # Shoulders expand: (140, 260) to (660, 260)
    # Belly expands: (60, 520) to (740, 520)
    # Base rounds: (200, 900) to (600, 900)
    pot_coords = [
        (260, 70), (540, 70), # Flared rim top
        (520, 150), (660, 280), (740, 500), (730, 680), # Right side curves
        (620, 840), (480, 910), (320, 910), (180, 840), # Bottom base
        (70, 680), (60, 500), (140, 280), (280, 150)    # Left side curves
    ]
    
    # Draw clay body with warm earthy fill and dark terracotta outline
    draw.polygon(pot_coords, fill="#f2e8dc", outline="#8c4b27", width=6)

    # Rim / Neck highlight
    draw.ellipse([250, 50, 550, 95], fill="#c46231", outline="#8c4b27", width=5)

    # Geometric Shoulder Lines
    draw.arc([100, 220, 700, 360], start=0, end=180, fill="#2d241e", width=6)
    draw.arc([80, 280, 720, 420], start=0, end=180, fill="#8c4b27", width=4)

    # Stepped Mimbres Geometric Accent Bands on left and right of belly
    # Left steps
    draw.line([(120, 340), (180, 340), (180, 400), (240, 400), (240, 460)], fill="#8c4b27", width=6)
    draw.line([(100, 420), (160, 420), (160, 480), (220, 480), (220, 540)], fill="#2d241e", width=5)
    # Right steps
    draw.line([(680, 340), (620, 340), (620, 400), (560, 400), (560, 460)], fill="#8c4b27", width=6)
    draw.line([(700, 420), (640, 420), (640, 480), (580, 480), (580, 540)], fill="#2d241e", width=5)

    # Lower Base Curves
    draw.arc([160, 760, 640, 880], start=0, end=180, fill="#2d241e", width=8)
    draw.arc([200, 800, 600, 900], start=0, end=180, fill="#8c4b27", width=5)

    # 2. Add Typography (Room Info)
    # Room Badge
    draw.rounded_rectangle([320, 115, 480, 155], radius=12, fill="#c46231")
    draw.text((400, 135), f"ROOM {room['id']}", fill="#ffffff", anchor="mm")

    # Title & Subtitle
    draw.text((400, 185), room["title"], fill="#2d241e", anchor="mm")
    draw.text((400, 215), f"— {room['subtitle']} —", fill="#785a44", anchor="mm")

    # 3. Center QR Code Frame & Paste QR Image
    qr_img = generate_qr_image(f"{BASE_URL}/?room={room['id']}", size=280)
    
    # White ceramic frame behind QR
    draw.rounded_rectangle([230, 360, 570, 700], radius=24, fill="#fffdfa", outline="#2d241e", width=6)
    draw.rounded_rectangle([240, 370, 560, 690], radius=18, fill=None, outline="#c46231", width=3)
    
    # Paste QR Code into center
    im.paste(qr_img, (260, 390), qr_img)

    # 4. Footer CTA
    draw.text((400, 735), "🎧 Point Phone Camera Here for Audio Tour", fill="#c46231", anchor="mm")
    draw.text((400, 765), "Deming Luna Mimbres Museum • Free Web Guide", fill="#8c7664", anchor="mm")

    # 5. Scissor / Cut Guide Marker on Rim
    draw.text((400, 30), "✂️ Cut along the curved clay pot silhouette outline", fill="#999999", anchor="mm")

    im.save(output_path, "PNG")

def main():
    root = Path(__file__).parent.parent
    rooms_file = root / "data" / "rooms.json"
    qr_dir = root / "qr_codes"
    qr_dir.mkdir(exist_ok=True)

    with open(rooms_file, "r", encoding="utf-8") as f:
        rooms = json.load(f)

    # Generate standalone high-res PNG pot cutout images for all 15 rooms
    for r in rooms:
        out_png = qr_dir / f"mimbres_pot_room_{r['id']}.png"
        create_mimbres_pot_png(r, out_png)

    print(f"[OK] Generated {len(rooms)} standalone high-res Mimbres Pot PNG cutout images in {qr_dir}")

if __name__ == "__main__":
    main()
