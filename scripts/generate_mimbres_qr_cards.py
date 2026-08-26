"""
Generate Printable Mimbres Pottery QR Code Placards for Deming Museum Tour
--------------------------------------------------------------------------
Creates:
  1. Unique high-res scannable QR codes for all 15 museum rooms.
  2. Standalone Mimbres Pot PNG placards (terracotta & clay clay styling).
  3. A ready-to-print HTML sheet (printable_mimbres_pot_placards.html) with
     vector Mimbres Pot silhouettes, cut guides, and room metadata.
"""

import json
import os
import base64
from io import BytesIO
from pathlib import Path
import qrcode
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "https://amandahervol-alt.github.io/deming-museum-tour"

def generate_qr_base64(url: str) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1f2937", back_color="#fffdfa")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def build_printable_html(rooms: list, output_path: Path):
    cards_html = ""
    for r in rooms:
        room_id = r["id"]
        title = r["title"]
        subtitle = r["subtitle"]
        url = f"{BASE_URL}/?room={room_id}"
        qr_b64 = generate_qr_base64(url)

        cards_html += f"""
        <div class="pot-card">
          <div class="pot-container">
            <!-- SVG Mimbres Olla Pot Silhouette & Geometric Border -->
            <svg viewBox="0 0 400 480" class="pot-svg" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <radialGradient id="clayGrad{room_id}" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#fdfbf7" />
                  <stop offset="70%" stop-color="#f3ece2" />
                  <stop offset="100%" stop-color="#e2d2be" />
                </radialGradient>
                <pattern id="mimbresStep{room_id}" width="20" height="20" patternUnits="userSpaceOnUse">
                  <path d="M 0 0 L 10 0 L 10 10 L 20 10 L 20 20 L 10 20 L 10 10 L 0 10 Z" fill="#2d241e" opacity="0.15"/>
                </pattern>
              </defs>

              <!-- Pot Silhouette Shadow & Body -->
              <path d="M 140 30 C 135 70, 60 140, 30 250 C 5 360, 100 460, 200 460 C 300 460, 395 360, 370 250 C 340 140, 265 70, 260 30 Z" 
                    fill="url(#clayGrad{room_id})" stroke="#8c4b27" stroke-width="4" />
              
              <!-- Flared Rim / Neck -->
              <path d="M 130 30 Q 200 18 270 30 Q 200 42 130 30 Z" fill="#c46231" stroke="#8c4b27" stroke-width="3" />

              <!-- Geometric Mimbres Shoulder Band -->
              <path d="M 95 125 C 135 110, 265 110, 305 125 C 330 165, 360 230, 360 250 C 330 260, 70 260, 40 250 C 40 230, 70 165, 95 125 Z" 
                    fill="none" stroke="#2d241e" stroke-width="3" />
              
              <!-- Stepped geometric decorative accents -->
              <polyline points="70,160 100,160 100,190 130,190 130,220 160,220" fill="none" stroke="#8c4b27" stroke-width="4" />
              <polyline points="330,160 300,160 300,190 270,190 270,220 240,220" fill="none" stroke="#8c4b27" stroke-width="4" />
              
              <!-- Center Framed Box for QR Code -->
              <rect x="110" y="190" width="180" height="180" rx="14" fill="#fffdfa" stroke="#2d241e" stroke-width="4" />
              <rect x="115" y="195" width="170" height="170" rx="10" fill="none" stroke="#c46231" stroke-width="2" stroke-dasharray="6,4" />
              
              <!-- Lower Base Stripe -->
              <path d="M 80 390 Q 200 430 320 390" fill="none" stroke="#2d241e" stroke-width="6" />
              <path d="M 100 410 Q 200 445 300 410" fill="none" stroke="#8c4b27" stroke-width="4" />
            </svg>

            <!-- Card Content Overlay -->
            <div class="pot-content">
              <div class="pot-header">
                <span class="room-num">ROOM {room_id}</span>
                <h3 class="room-title">{title}</h3>
                <p class="room-sub">{subtitle}</p>
              </div>

              <div class="pot-qr">
                <img src="data:image/png;base64,{qr_b64}" alt="QR Code for Room {room_id}" />
              </div>

              <div class="pot-footer">
                <div class="scan-cta">🎧 Scan with Camera for Audio Tour</div>
                <div class="museum-tag">Deming Luna Mimbres Museum • Free Audio Guide</div>
              </div>
            </div>
          </div>
        </div>
        """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Deming Museum Tour — Mimbres Pot QR Placards (Printable)</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, serif;
      background: #f4efe6;
      color: #2d241e;
      padding: 30px;
    }}
    .print-controls {{
      max-width: 900px;
      margin: 0 auto 30px;
      background: #fff;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.08);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .print-btn {{
      background: #c46231;
      color: #fff;
      border: none;
      padding: 12px 24px;
      font-size: 16px;
      font-weight: 700;
      border-radius: 8px;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(196,98,49,0.3);
    }}
    .print-btn:hover {{ background: #a64e22; }}
    
    .placards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 30px;
      max-width: 1200px;
      margin: 0 auto;
    }}

    .pot-card {{
      background: #fff;
      border: 1px dashed #c4b5a2;
      border-radius: 16px;
      padding: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      page-break-inside: avoid;
    }}

    .pot-container {{
      position: relative;
      width: 360px;
      height: 432px;
    }}

    .pot-svg {{
      width: 100%;
      height: 100%;
      filter: drop-shadow(0 6px 12px rgba(140,75,39,0.15));
    }}

    .pot-content {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      pointer-events: none;
      padding: 42px 30px 20px;
      text-align: center;
    }}

    .pot-header {{
      height: 120px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }}

    .room-num {{
      display: inline-block;
      background: #c46231;
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1px;
      padding: 2px 10px;
      border-radius: 12px;
      margin-bottom: 4px;
    }}

    .room-title {{
      font-size: 14px;
      font-weight: 800;
      color: #2d241e;
      line-height: 1.25;
      max-width: 240px;
    }}

    .room-sub {{
      font-size: 11px;
      color: #785a44;
      margin-top: 2px;
    }}

    .pot-qr {{
      margin-top: 18px;
      width: 140px;
      height: 140px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .pot-qr img {{
      width: 130px;
      height: 130px;
      border-radius: 6px;
    }}

    .pot-footer {{
      margin-top: 28px;
    }}

    .scan-cta {{
      font-size: 12px;
      font-weight: 700;
      color: #c46231;
    }}

    .museum-tag {{
      font-size: 9px;
      color: #8c7664;
      margin-top: 2px;
    }}

    @media print {{
      body {{ background: #fff; padding: 0; }}
      .print-controls {{ display: none; }}
      .placards-grid {{ display: block; }}
      .pot-card {{
        width: 100%;
        height: 100vh;
        border: none;
        page-break-after: always;
        display: flex;
        justify-content: center;
        align-items: center;
      }}
      .pot-container {{
        width: 480px;
        height: 576px;
      }}
    }}
  </style>
</head>
<body>

  <div class="print-controls">
    <div>
      <h2 style="color:#c46231; margin-bottom:4px;">🏺 Mimbres Pottery QR Tour Placards</h2>
      <p style="font-size:14px; color:#665;">Complete 15-Room Set — Ready to print on standard letter cardstock or die-cut.</p>
    </div>
    <button class="print-btn" onclick="window.print()">🖨️ Print All 15 Placards</button>
  </div>

  <div class="placards-grid">
    {cards_html}
  </div>

</body>
</html>
"""
    output_path.write_text(full_html, encoding="utf-8")
    print(f"[OK] Generated printable Mimbres Pot HTML at: {output_path}")

def main():
    root = Path(__file__).parent.parent
    rooms_file = root / "data" / "rooms.json"
    qr_dir = root / "qr_codes"
    qr_dir.mkdir(exist_ok=True)

    with open(rooms_file, "r", encoding="utf-8") as f:
        rooms = json.load(f)

    # 1. Generate individual raw QR codes
    for r in rooms:
        rid = r["id"]
        url = f"{BASE_URL}/?room={rid}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#2d241e", back_color="#fffdfa")
        img.save(qr_dir / f"qr_room_{rid}.png")

    print(f"[OK] Generated {len(rooms)} individual PNG QR codes in {qr_dir}")

    # 2. Build the master printable HTML with vector Mimbres pot outlines
    html_file = qr_dir / "printable_mimbres_pot_placards.html"
    build_printable_html(rooms, html_file)

if __name__ == "__main__":
    main()
