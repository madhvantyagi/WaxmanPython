import sys
import subprocess
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "youtube-transcript-api"])
    from youtube_transcript_api import YouTubeTranscriptApi

import os

video_ids = [
    "kV-mdyOyW7Y",
    "egqaYa-PFWY",
    "ABZ2fq-IqLA",
    "EO2Y-QwEmmY",
    "2H-Caft_zHg",
    "Lzq7JPfsGFw",
    "CtaLHpsbrXE"
]

out_dir = "/Users/choclate/Desktop/Waxman python "

for vid in video_ids:
    try:
        ts = YouTubeTranscriptApi.get_transcript(vid)
        text = " ".join([t['text'] for t in ts])
        with open(os.path.join(out_dir, f"{vid}.txt"), "w") as f:
            f.write(text)
        print(f"Success: {vid}")
    except Exception as e:
        print(f"Error {vid}: {e}")
