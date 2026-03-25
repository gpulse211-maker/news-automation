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

for i, e in enumerate(feed.entries[:3]):
    title = clean(e.title)

    wrapped_title = "\\n".join(textwrap.wrap(title, width=28))

    name = f"video_{i}_{datetime.now().strftime('%H%M%S')}"
    video = f"{OUTPUT}/{name}.mp4"

    cmd = f"""
    ffmpeg -y -f lavfi -i color=c=black:s=1080x1920:d=12 \
    -vf "
    scale=1080:1920,

    # animated background effect
    geq=r='(X/W)*255':g='(Y/H)*255':b='128',

    # TOP RED BAR
    drawbox=y=0:color=red@0.9:width=iw:height=150:t=fill,

    drawtext=text='BREAKING NEWS':fontcolor=white:fontsize=60:
    x=(w-text_w)/2:y=40,

    # CENTER HEADLINE
    drawtext=text='{wrapped_title}':fontcolor=white:fontsize=50:
    x=(w-text_w)/2:y=(h/2)-150:line_spacing=12,

    # BOTTOM TICKER BAR
    drawbox=y=h-200:color=blue@0.8:width=iw:height=200:t=fill,

    drawtext=text='LIVE • WORLD NEWS • UPDATES':
    fontcolor=white:fontsize=40:x=(w-text_w)/2:y=h-140
    " \
    -pix_fmt yuv420p {video}
    """

    subprocess.call(cmd, shell=True)

print("DONE: TV-style videos created")
