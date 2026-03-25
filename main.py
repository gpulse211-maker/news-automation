import feedparser
import os
import subprocess
from datetime import datetime
import textwrap

OUTPUT = "output"
os.makedirs(OUTPUT, exist_ok=True)

# Get news
feed = feedparser.parse("http://feeds.bbci.co.uk/news/world/rss.xml")

def clean(t):
    return t.replace(":", "").replace("'", "").replace(",", "")

for i, e in enumerate(feed.entries[:3]):
    title = clean(e.title)

    # Keep your same structure
    line1 = "BREAKING NEWS"
    line2 = title[:80]
    line3 = "This is getting global attention"
    line4 = "Follow for more updates"

    # ✅ FIX: wrap long text properly
    wrapped_title = "\\n".join(textwrap.wrap(line2, width=28))

    name = f"video_{i}_{datetime.now().strftime('%H%M%S')}"
    video = f"{OUTPUT}/{name}.mp4"

    cmd = f"""
    ffmpeg -y -f lavfi -i color=c=black:s=1080x1920:d=12 \
    -vf "
    scale=1080:1920,

    drawbox=y=0:color=red@0.9:width=iw:height=140:t=fill,

    drawtext=text='{line1}':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=30,

    drawtext=text='{wrapped_title}':fontcolor=white:fontsize=52:x=(w-text_w)/2:y=(h/2)-120:line_spacing=10,

    drawtext=text='{line3}':fontcolor=white:fontsize=42:x=(w-text_w)/2:y=(h/2)+80,

    drawtext=text='{line4}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=(h/2)+150
    " \
    -pix_fmt yuv420p {video}
    """

    subprocess.call(cmd, shell=True)

print("DONE: Fixed videos created")
