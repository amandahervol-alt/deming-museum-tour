import os
import shutil
import json

dl = r"C:\Users\manet\Downloads"

# 1. Copy Quilt/Lace Room audio
# Let's check the most recent Elise Hart audio (1:27)
quilt_src = os.path.join(dl, "ElevenLabs_2026-09-19T15_17_30_Elise Hart - Warm, Clear & Engaging_pvc_sp100_s50_sb75_se0_b_m2.mp3")
if not os.path.exists(quilt_src):
    quilt_src = os.path.join(dl, "ElevenLabs_2026-09-19T15_17_30_Elise Hart - Warm, Clear & Engaging_pvc_sp100_s50_sb75_se0_b_m2 (1).mp3")

if os.path.exists(quilt_src):
    shutil.copy2(quilt_src, "audio/room_10.mp3")
    print(f"Copied {quilt_src} -> audio/room_10.mp3 ({os.path.getsize('audio/room_10.mp3')} bytes)")

# 2. Update rooms.json
with open("data/rooms.json", "r", encoding="utf-8") as f:
    rooms = json.load(f)

for r in rooms:
    if r["id"] == 10:
        r["title"] = "Quilt & Lace Room"
        r["subtitle"] = "Hand-Stitched Heritage, 1820s Spreads & Lottie Deno Lace"
        r["audio"] = "audio/room_10.mp3"
        r["duration"] = "1:27"
        r["transcript"] = "European settlers — the Dutch and English among them — brought the tradition of quilting to America in the 17th century. Early quilts were practical creations, often pieced together from fabric scraps and recycled clothing. Over time, quilting bees became cherished social gatherings, giving women a chance to work side by side, trade stories, and strengthen the bonds of their community. The oldest quilt in this room is a hand-woven spread dating to around 1820, donated in memory of Bessie Gomer May, the woman largely responsible for this museum's existence. Look closely and you'll also find fine examples of tatting lace, made from an intricate series of knots and loops. One piece of particular interest is an altar cloth made by Lottie 'Deno' Thurman — known formally as Mrs. Frank Thurman. Lottie led a colorful life in Deming and was renowned as a remarkably shrewd gambler; her reputation was so notable that she's said to have inspired the character of Miss Kitty on the television series Gunsmoke. Several books on Lottie Deno's life are available online, or ask about them in our Gift Store."
        r["highlights"] = [
            "17th-Century Quilting Traditions & Quilting Bees",
            "Circa 1820 Hand-Woven Spread (Bessie Gomer May Memorial)",
            "Intricate Tatting Lace Knots & Loops",
            "Lottie 'Deno' Thurman Handcrafted Altar Cloth",
            "Inspiration for Miss Kitty of TV's Gunsmoke"
        ]

with open("data/rooms.json", "w", encoding="utf-8") as f:
    json.dump(rooms, f, indent=2, ensure_ascii=False)

print("Updated data/rooms.json successfully.")

# 3. Update museum_knowledge.json
with open("data/museum_knowledge.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

knowledge["key_collections"]["quilt_collection"] = {
    "size": "One of the largest hand-stitched quilt displays in the American Southwest.",
    "eras": "Mid-1800s to 1950s",
    "popular_styles": "Crazy Quilts, Log Cabin, Wedding Ring, feedsack fabrics, tatting lace.",
    "oldest_quilt": "Hand-woven spread circa 1820 donated in memory of Bessie Gomer May, key founder of the museum.",
    "lottie_deno_thurman": "Intricate tatting lace altar cloth handcrafted by Mrs. Frank Thurman (Lottie Deno), famous frontier gambler who inspired Miss Kitty in Gunsmoke.",
    "narrator": "Elise Hart"
}

with open("data/museum_knowledge.json", "w", encoding="utf-8") as f:
    json.dump(knowledge, f, indent=2, ensure_ascii=False)

print("Updated data/museum_knowledge.json successfully.")
