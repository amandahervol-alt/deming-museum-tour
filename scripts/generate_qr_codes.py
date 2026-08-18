#!/usr/bin/env python3
"""
Deming Luna Mimbres Museum - QR Code Generator Script
Generates 15 high-resolution QR codes linking to each room's GitHub Pages audio tour page.

Usage:
  python generate_qr_codes.py --base-url "https://YOUR_GITHUB_USERNAME.github.io/deming-museum-tour"
"""

import os
import argparse
import urllib.parse

def generate_qr_codes(base_url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating 15 QR Codes for Base URL: {base_url}")
    print(f"Output Directory: {os.path.abspath(output_dir)}")
    print("-" * 60)

    try:
        import qrcode
        has_qrcode_lib = True
    except ImportError:
        has_qrcode_lib = False
        print("Note: 'qrcode' python package not installed. Generating SVG QR code placeholders.")
        print("Tip: Install qrcode via: pip install qrcode pillow")

    for room_id in range(1, 16):
        target_url = f"{base_url.rstrip('/')}/?room={room_id}"
        
        if has_qrcode_lib:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(target_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#8C2D19", back_color="white")
            filename = os.path.join(output_dir, f"room_{room_id}_qr.png")
            img.save(filename)
            print(f"[OK] Room {room_id:02d} PNG -> {filename} ({target_url})")
        else:
            # Generate printable HTML/SVG fallback file
            encoded_url = urllib.parse.quote(target_url)
            qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&color=8C2D19&data={encoded_url}"
            filename = os.path.join(output_dir, f"room_{room_id}_qr.html")
            with open(filename, 'w') as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
  <title>Room {room_id} QR Code - Deming Museum</title>
  <style>
    body {{ font-family: sans-serif; text-align: center; padding: 40px; background: #FAF6F0; }}
    .card {{ background: white; padding: 30px; border-radius: 12px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 2px solid #8C2D19; }}
    h2 {{ color: #8C2D19; margin-bottom: 5px; }}
    p {{ color: #666; font-size: 14px; margin-bottom: 20px; }}
    img {{ width: 250px; height: 250px; }}
    .url {{ margin-top: 15px; font-family: monospace; font-size: 12px; color: #444; }}
  </style>
</head>
<body>
  <div class="card">
    <h2>Deming Luna Mimbres Museum</h2>
    <p>Scan to hear Room {room_id} Audio Speech & Guide</p>
    <img src="{qr_api_url}" alt="Room {room_id} QR Code" />
    <div class="url">{target_url}</div>
  </div>
</body>
</html>""")
            print(f"[OK] Room {room_id:02d} Printable HTML -> {filename}")

    print("-" * 60)
    print("Done! QR Codes successfully created.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Museum Room QR Codes")
    parser.add_argument("--base-url", default="https://username.github.io/deming-museum-tour", help="GitHub Pages Base URL")
    parser.add_argument("--output-dir", default="../qr_codes", help="Output directory for QR code images")
    args = parser.parse_args()
    
    generate_qr_codes(args.base_url, args.output_dir)
