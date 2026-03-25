import feedparser
import os
import subprocess
from datetime import datetime
import textwrap

RSS_URL = "http://feeds.bbci.co.uk/news/world/rss.xml"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

feed = feedparser.parse(RSS_URL)

def clean_text(text):
    return text.replace(":", "").replace("'", "").replace(",", "")

for i, entry in enumerate(feed.entries[:3]):
    title = clean_text(entry.title)

    # Better script
    script = f"""
BREAKING NEWS

{title}

This is happening right now.

Global impact is expected.

Follow for more updates.
"""

    wrapped = "\\n".join(textwrap.wrap(script, width=30))

    filename = f"news_{i}_{datetime.now().strftime('%H%M%S')}"
    video_path = os.path.join(OUTPUT_DIR, filename + ".mp4")

    # Animated background (moving effect)
    cmd = f'''
    ffmpeg -y -f lavfi -i color=c=black:s=1080x1920:d=12 \
    -vf "drawbox=x=0:y=0:w=iw:h=200:color=red@0.8:t=fill,\
    drawtext=text='{wrapped}':fontcolor=white:fontsize=42:x=50:y=300:line_spacing=12" \
    -pix_fmt yuv420p {video_path}
    '''

    subprocess.call(cmd, shell=True)

print("Better videos created")
