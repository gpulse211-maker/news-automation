import feedparser
import os
import subprocess
from datetime import datetime

OUTPUT = "output"
os.makedirs(OUTPUT, exist_ok=True)

feed = feedparser.parse("http://feeds.bbci.co.uk/news/world/rss.xml")

def clean(t):
    return t.replace(":", "").replace("'", "").replace(",", "")

for i, e in enumerate(feed.entries[:3]):
    title = clean(e.title)

    # Better viral-style script
    line1 = "THIS JUST HAPPENED"
    line2 = title[:60]
    line3 = "This is getting global attention"
    line4 = "More updates coming soon"

    name = f"video_{i}_{datetime.now().strftime('%H%M%S')}"
    video = f"{OUTPUT}/{name}.mp4"

    cmd = f"""
    ffmpeg -y -f lavfi -i color=c=black:s=1080x1920:d=12 \
    -vf "
    drawbox=y=0:color=red@0.9:width=iw:height=180:t=fill,

    drawtext=text='{line1}':fontcolor=white:fontsize=70:x=(w-text_w)/2:y=60,

    drawtext=text='{line2}':fontcolor=white:fontsize=46:x=60:y=500,

    drawtext=text='{line3}':fontcolor=white:fontsize=40:x=60:y=800,

    drawtext=text='{line4}':fontcolor=white:fontsize=36:x=60:y=1100
    " \
    -pix_fmt yuv420p {video}
    """

    subprocess.call(cmd, shell=True)

print("FINAL: Better videos generated")
