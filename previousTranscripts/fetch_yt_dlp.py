import os
import sys
import subprocess

# Install yt-dlp if needed
try:
    import yt_dlp
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "yt-dlp"])
    import yt_dlp

# Install webvtt-py if needed
try:
    import webvtt
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "webvtt-py"])
    import webvtt

video_ids = [
    "kV-mdyOyW7Y",
    "egqaYa-PFWY",
    "ABZ2fq-IqLA",
    "EO2Y-QwEmmY",
    "2H-Caft_zHg",
    "Lzq7JPfsGFw",
    "CtaLHpsbrXE"
]

ydl_opts = {
    'skip_download': True,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'outtmpl': '/Users/choclate/Desktop/Waxman python /%(id)s.%(ext)s'
}

print("Downloading subtitles...")
for vid in video_ids:
    url = f"https://www.youtube.com/watch?v={vid}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Convert VTTs to clean text
print("\nConverting to clean text...")
out_dir = "/Users/choclate/Desktop/Waxman python "
for vid in video_ids:
    vtt_path = os.path.join(out_dir, f"{vid}.en.vtt")
    txt_path = os.path.join(out_dir, f"{vid}_transcript.txt")
    if os.path.exists(vtt_path):
        try:
            vtt = webvtt.read(vtt_path)
            lines = []
            for caption in vtt:
                text = caption.text.strip()
                # Remove styling tags if present
                if text and text not in lines:
                    lines.append(text)
            with open(txt_path, 'w') as f:
                f.write("\n".join(lines))
            print(f"Extracted {txt_path}")
        except Exception as e:
            print(f"Error parsing {vtt_path}: {e}")
    else:
        print(f"Missing {vtt_path}")
