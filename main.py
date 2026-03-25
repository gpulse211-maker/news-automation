import feedparser
import os
import subprocess
from datetime import datetime
import textwrap

OUTPUT = "output"
os.makedirs(OUTPUT, exist_ok=True)

feed = feedparser.parse("http://feeds.bbci.co.uk/news/world/rss.xml")

def clean(t):
    return t.replace(":", "").replace("'", "").replace(",", "")

for i, e in enumerate(feed.entries[:2]):  # keep small for testing
    title = clean(e.title)

    wrapped = "\\n".join(textwrap.wrap(title, width=28))

    name = f"video_{i}_{datetime.now().strftime('%H%M%S')}"
    video = f"{OUTPUT}/{name}.mp4"

    # IMPORTANT: single-line filter (GitHub safe)
    filter_text = (
        "drawbox=y=0:color=red@0.9:width=iw:height=140:t=fill,"
        "drawtext=text='BREAKING NEWS':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=30,"
        f"drawtext=text='{wrapped}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h/2)-120:line_spacing=10,"
        "drawbox=y=h-180:color=blue@0.8:width=iw:height=180:t=fill,"
        "drawtext=text='LIVE NEWS UPDATE':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=h-120"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "lavfi",
        "-i", "color=c=black:s=1080x1920:d=10",
        "-vf", filter_text,
        "-pix_fmt", "yuv420p",
        video
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # DEBUG (VERY IMPORTANT)
    print(result.stdout)
    print(result.stderr)

print("DONE")
