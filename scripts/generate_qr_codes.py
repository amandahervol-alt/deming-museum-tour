#!/usr/bin/env python3
"""
Deming Luna Mimbres Museum - QR Code Generator Script
Generates 15 high-resolution QR code images and printable placard HTML files
including each room's narration script, highlights, and direct QR links.

Usage:
  python generate_qr_codes.py --base-url "https://amandahervol-alt.github.io/deming-museum-tour"
"""

import os
import json
import base64
import argparse
from io import BytesIO
from pathlib import Path
import qrcode

DEFAULT_BASE_URL = "https://amandahervol-alt.github.io/deming-museum-tour"

def generate_qr_codes(base_url, output_dir, data_file):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with open(data_file, "r", encoding="utf-8") as f:
        rooms = json.load(f)

    print(f"Generating QR Codes & Script Cards for {len(rooms)} Rooms...")
    print(f"Base URL: {base_url}")
    print(f"Output Directory: {output_path.resolve()}")
    print("-" * 60)

    for room in rooms:
        room_id = room["id"]
        title = room["title"]
        subtitle = room.get("subtitle", "")
        transcript = room.get("transcript", "")
        duration = room.get("duration", "2:00")
        highlights = room.get("highlights", [])
        
        target_url = f"{base_url.rstrip('/')}/?room={room_id}"

        # 1. Generate QR Code PNG
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(target_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#8C2D19", back_color="#FFFDF9")
        
        png_path = output_path / f"room_{room_id}_qr.png"
        img.save(png_path)

        # Base64 string for embedding into HTML card
        buf = BytesIO()
        img.save(buf, format="PNG")
        qr_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        # Specific narrator credit if applicable
        narrator_credit = "Narrated by Kirk Hunter" if room_id == 1 else "Interactive Audio Tour"

        # 2. Build Printable HTML Card with Full Narration Script
        highlights_html = "".join(f'<span class="badge">{h}</span>' for h in highlights)

        card_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Room {room_id} Exhibit Placard & Narration Script - Deming Museum</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, serif;
      background: #f4ede4;
      color: #2c221e;
      padding: 30px 16px;
      line-height: 1.5;
    }}
    .print-bar {{
      max-width: 720px;
      margin: 0 auto 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .btn-print {{
      background: #8c2d19;
      color: #fff;
      border: none;
      padding: 10px 20px;
      font-size: 15px;
      font-weight: 700;
      border-radius: 8px;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(140, 45, 25, 0.25);
    }}
    .btn-print:hover {{ background: #702111; }}
    .placard-card {{
      max-width: 720px;
      margin: 0 auto;
      background: #fffdf9;
      border: 3px solid #8c2d19;
      border-radius: 16px;
      padding: 36px 32px;
      box-shadow: 0 10px 30px rgba(70, 35, 15, 0.12);
    }}
    .header {{
      text-align: center;
      border-bottom: 2px dashed #d9c5b2;
      padding-bottom: 20px;
      margin-bottom: 24px;
    }}
    .museum-name {{
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: #8c2d19;
      font-weight: 800;
      margin-bottom: 6px;
    }}
    .room-badge {{
      display: inline-block;
      background: #8c2d19;
      color: white;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 14px;
      border-radius: 20px;
      margin-bottom: 8px;
    }}
    .room-title {{
      font-size: 26px;
      font-weight: 800;
      color: #2c221e;
      margin-bottom: 4px;
    }}
    .room-subtitle {{
      font-size: 15px;
      color: #7a5c48;
      font-style: italic;
    }}
    .qr-section {{
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 26px;
      text-align: center;
    }}
    .qr-box {{
      background: white;
      padding: 14px;
      border: 2px solid #8c2d19;
      border-radius: 14px;
      box-shadow: 0 4px 16px rgba(140, 45, 25, 0.1);
      margin-bottom: 12px;
    }}
    .qr-box img {{
      width: 180px;
      height: 180px;
      display: block;
    }}
    .scan-guide {{
      font-size: 14px;
      font-weight: 700;
      color: #8c2d19;
      margin-bottom: 4px;
    }}
    .narrator-tag {{
      font-size: 12px;
      color: #634b3c;
      background: #f1e4d6;
      padding: 2px 10px;
      border-radius: 6px;
      font-weight: 600;
      display: inline-block;
    }}
    .highlights-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      justify-content: center;
      margin: 14px 0 20px;
    }}
    .badge {{
      background: #f3ece4;
      color: #593e2f;
      font-size: 11px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 6px;
      border: 1px solid #dfd1c3;
    }}
    .script-section {{
      background: #faf4ed;
      border-radius: 12px;
      padding: 20px 24px;
      border-left: 4px solid #8c2d19;
    }}
    .script-heading {{
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #8c2d19;
      font-weight: 800;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .script-text {{
      font-size: 14.5px;
      line-height: 1.65;
      color: #3b2c24;
      text-align: justify;
    }}
    .url-footer {{
      margin-top: 20px;
      text-align: center;
      font-size: 11px;
      font-family: monospace;
      color: #8c7664;
    }}
    @media print {{
      body {{ background: white; padding: 0; }}
      .print-bar {{ display: none; }}
      .placard-card {{ box-shadow: none; border: 2px solid #8c2d19; max-width: 100%; }}
    }}
  </style>
</head>
<body>

  <div class="print-bar">
    <a href="{target_url}" target="_blank" style="color:#8c2d19; text-decoration:none; font-weight:600;">← Open Interactive Tour Page</a>
    <button class="btn-print" onclick="window.print()">🖨️ Print Exhibit Placard</button>
  </div>

  <div class="placard-card">
    <header class="header">
      <div class="museum-name">Deming Luna Mimbres Museum</div>
      <div class="room-badge">Room {room_id} of 15</div>
      <h1 class="room-title">{title}</h1>
      <p class="room-subtitle">{subtitle}</p>
    </header>

    <div class="qr-section">
      <div class="qr-box">
        <img src="data:image/png;base64,{qr_b64}" alt="QR Code for Room {room_id}" />
      </div>
      <div class="scan-guide">📱 Point Smartphone Camera to Listen</div>
      <div class="narrator-tag">🎙️ {narrator_credit} • Duration: {duration}</div>
    </div>

    <div class="highlights-row">
      {highlights_html}
    </div>

    <div class="script-section">
      <div class="script-heading">
        <span>📖 Audio Speech Narration Script</span>
        <span style="font-weight:600; font-size:11px; color:#7a5c48;">{duration}</span>
      </div>
      <p class="script-text">{transcript}</p>
    </div>

    <div class="url-footer">
      Direct Link: {target_url}
    </div>
  </div>

</body>
</html>"""

        html_path = output_path / f"room_{room_id}_qr.html"
        html_path.write_text(card_html, encoding="utf-8")
        print(f"[OK] Generated Room {room_id:02d} QR Code & Script Card -> {html_path.name}")

    print("-" * 60)
    print("All 15 QR Codes & Script Cards generated successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Museum Room QR Codes & Scripts")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="GitHub Pages Base URL")
    parser.add_argument("--output-dir", default=None, help="Output directory for QR code images")
    parser.add_argument("--data-file", default=None, help="Path to rooms.json")
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    
    out_dir = Path(args.output_dir) if args.output_dir else base_dir / "qr_codes"
    data_path = Path(args.data_file) if args.data_file else base_dir / "data" / "rooms.json"

    generate_qr_codes(args.base_url, out_dir, data_path)
