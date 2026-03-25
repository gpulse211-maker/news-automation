import feedparser
import os
import subprocess
from datetime import datetime

RSS_URL = "http://feeds.bbci.co.uk/news/world/rss.xml"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

feed = feedparser.parse(RSS_URL)

def clean_text(text):
    return text.replace(":", "").replace("'", "").replace(",", "")

for i, entry in enumerate(feed.entries[:3]):
    title = clean_text(entry.title)

    filename = f"news_{i}_{datetime.now().strftime('%H%M%S')}"
    video_path = os.path.join(OUTPUT_DIR, filename + ".mp4")

    # Split text into lines (for timing effect)
    line1 = "BREAKING NEWS"
    line2 = title[:60]
    line3 = "This is happening right now"
    line4 = "Follow for more updates"

    cmd = f'''
    ffmpeg -y -f lavfi -i color=c=black:s=1080x1920:d=12 \
    -vf "
    drawbox=y=0:color=red@0.8:width=iw:height=150:t=fill,
    drawtext=text='{line1}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=40:enable='between(t,0,12)',

    drawtext=text='{line2}':fontsize=42:fontcolor=white:x=60:y=400:enable='between(t,1,5)',
    drawtext=text='{line3}':fontsize=42:fontcolor=white:x=60:y=600:enable='between(t,5,9)',
    drawtext=text='{line4}':fontsize=42:fontcolor=white:x=60:y=800:enable='between(t,9,12)'
    " \
    -pix_fmt yuv420p {video_path}
    '''

    subprocess.call(cmd, shell=True)

print("Fixed: videos now have timing and flow")
