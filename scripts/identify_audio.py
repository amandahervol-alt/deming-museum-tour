import os, glob

# Let's inspect the files in Downloads
dl = r"C:\Users\manet\Downloads"
files = glob.glob(os.path.join(dl, "*.mp3"))
files.sort(key=os.path.getmtime, reverse=True)

print("Recent MP3s in Downloads:")
for f in files[:10]:
    print(f"{os.path.getmtime(f)} | {os.path.getsize(f):>10} | {os.path.basename(f)}")
