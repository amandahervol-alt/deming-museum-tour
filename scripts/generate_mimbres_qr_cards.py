"""
Generate Printable Mimbres Pottery QR Code Placards for Deming Museum Tour
--------------------------------------------------------------------------
"""

import json
import base64
from io import BytesIO
from pathlib import Path
import qrcode

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
    img = qr.make_image(fill_color="#231c17", back_color="#fffdf8")
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
          <div class="scissor-guide">✂️ <em>Cut along outer pot curve</em></div>
          <div class="pot-container">
            <!-- SVG Mimbres Olla Pot Silhouette -->
            <svg viewBox="0 0 400 480" class="pot-svg" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <radialGradient id="clayGrad{room_id}" cx="50%" cy="45%" r="55%">
                  <stop offset="0%" stop-color="#fffcf7" />
                  <stop offset="65%" stop-color="#f6ede1" />
                  <stop offset="100%" stop-color="#e0ceb7" />
                </radialGradient>
              </defs>

              <!-- Outer Scissor Cut Outline -->
              <path d="M 140 25 C 135 70, 60 140, 30 250 C 5 360, 100 460, 200 460 C 300 460, 395 360, 370 250 C 340 140, 265 70, 260 25 Z" 
                    fill="none" stroke="#a38870" stroke-width="2" stroke-dasharray="6,4" />

              <!-- Main Ceramic Pot Body -->
              <path d="M 140 30 C 135 70, 60 140, 30 250 C 5 360, 100 455, 200 455 C 300 455, 395 360, 370 250 C 340 140, 265 70, 260 30 Z" 
                    fill="url(#clayGrad{room_id})" stroke="#8c4b27" stroke-width="5" />
              
              <!-- Flared Rim Neck -->
              <path d="M 130 30 Q 200 15 270 30 Q 200 45 130 30 Z" fill="#c46231" stroke="#8c4b27" stroke-width="4" />

              <!-- Geometric Mimbres Shoulder Band -->
              <path d="M 95 130 C 135 115, 265 115, 305 130 C 330 170, 360 235, 360 255 C 330 265, 70 265, 40 255 C 40 235, 70 170, 95 130 Z" 
                    fill="none" stroke="#2d241e" stroke-width="4" />
              
              <!-- Stepped geometric decorative accents on shoulders -->
              <polyline points="70,165 100,165 100,195 130,195 130,225 160,225" fill="none" stroke="#8c4b27" stroke-width="5" />
              <polyline points="330,165 300,165 300,195 270,195 270,225 240,225" fill="none" stroke="#8c4b27" stroke-width="5" />
              
              <!-- Center Framed Box for QR Code -->
              <rect x="110" y="190" width="180" height="180" rx="18" fill="#fffdfa" stroke="#2d241e" stroke-width="5" />
              <rect x="116" y="196" width="168" height="168" rx="12" fill="none" stroke="#c46231" stroke-width="2" stroke-dasharray="5,3" />
              
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
                <div class="scan-cta">🎧 Point Camera for Audio Tour</div>
                <div class="museum-tag">Deming Luna Mimbres Museum</div>
              </div>
            </div>
          </div>
        </div>
        """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Deming Museum Tour — Mimbres Pot Shaped QR Placards</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, serif;
      background: #e8ded1;
      color: #2d241e;
      padding: 30px 20px;
    }}
    .print-controls {{
      max-width: 900px;
      margin: 0 auto 30px;
      background: #fff;
      padding: 22px 26px;
      border-radius: 14px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.08);
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
      box-shadow: 0 3px 10px rgba(196,98,49,0.35);
      transition: background 0.15s;
    }}
    .print-btn:hover {{ background: #a64e22; }}
    
    .placards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 40px;
      max-width: 1280px;
      margin: 0 auto;
    }}

    .pot-card {{
      display: flex;
      flex-direction: column;
      align-items: center;
      page-break-inside: avoid;
    }}

    .scissor-guide {{
      font-size: 12px;
      color: #8c7664;
      margin-bottom: 8px;
      font-weight: 600;
    }}

    .pot-container {{
      position: relative;
      width: 380px;
      height: 456px;
    }}

    .pot-svg {{
      width: 100%;
      height: 100%;
      filter: drop-shadow(0 10px 20px rgba(100,50,20,0.18));
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
      padding: 3px 12px;
      border-radius: 12px;
      margin-bottom: 4px;
    }}

    .room-title {{
      font-size: 15px;
      font-weight: 800;
      color: #2d241e;
      line-height: 1.25;
      max-width: 250px;
    }}

    .room-sub {{
      font-size: 11px;
      color: #785a44;
      margin-top: 3px;
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
      font-size: 13px;
      font-weight: 700;
      color: #c46231;
    }}

    .museum-tag {{
      font-size: 10px;
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
      <p style="font-size:14px; color:#665;">Complete 15-Room Set — Ready to print or cut out in the shape of a Mimbres clay pot!</p>
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

def main():
    root = Path(__file__).parent.parent
    rooms_file = root / "data" / "rooms.json"
    qr_dir = root / "qr_codes"
    qr_dir.mkdir(exist_ok=True)

    with open(rooms_file, "r", encoding="utf-8") as f:
        rooms = json.load(f)

    html_file = qr_dir / "printable_mimbres_pot_placards.html"
    build_printable_html(rooms, html_file)
    print(f"[OK] Re-generated printable HTML at: {html_file}")

if __name__ == "__main__":
    main()
