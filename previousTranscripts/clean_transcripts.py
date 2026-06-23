import os
import re

out_dir = "/Users/choclate/Desktop/Waxman python "
video_ids = [
    "kV-mdyOyW7Y",
    "egqaYa-PFWY",
    "ABZ2fq-IqLA",
    "EO2Y-QwEmmY",
    "2H-Caft_zHg",
    "Lzq7JPfsGFw",
    "CtaLHpsbrXE"
]

for vid in video_ids:
    path = os.path.join(out_dir, f"{vid}_transcript.txt")
    if os.path.exists(path):
        with open(path, 'r') as f:
            lines = f.readlines()
        
        clean_lines = []
        last_line = ""
        for line in lines:
            ll = line.strip()
            if ll and ll != last_line:
                clean_lines.append(ll)
                last_line = ll
                
        text = " ".join(clean_lines)
        # break into chunks of reasonable paragraph sizes or sentence endings
        text = re.sub(r'(?<=[.!?]) +', '\n\n', text)
        
        # wrap nicely
        import textwrap
        wrapped = textwrap.fill(text, width=80)
        
        with open(os.path.join(out_dir, f"{vid}_clean.txt"), 'w') as f:
            f.write(wrapped)
        print(f"Cleaned {vid}")
