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

    cmd = f'''
    ffmpeg -y -f lavfi -i color=c=black:s=1080x1920:d=10 \
    -vf "drawtext=text='BREAKING NEWS':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=200,\
    drawtext=text='{title}':fontcolor=white:fontsize=40:x=50:y=600" \
    -pix_fmt yuv420p {video_path}
    '''

    subprocess.call(cmd, shell=True)

print("Videos created")
