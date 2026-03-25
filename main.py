import feedparser
import os
import subprocess
from datetime import datetime
import pyttsx3

RSS_URL = "http://feeds.bbci.co.uk/news/world/rss.xml"
OUTPUT_DIR = "output"
BG_VIDEO = "bg.mp4"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Init voice
engine = pyttsx3.init()
engine.setProperty('rate', 165)

# Try female voice
for v in engine.getProperty('voices'):
    if "female" in v.name.lower():
        engine.setProperty('voice', v.id)
        break

feed = feedparser.parse(RSS_URL)

def clean(text):
    return text.replace(":", "").replace("'", "").replace(",", "")

for i, entry in enumerate(feed.entries[:3]):
    title = clean(entry.title)

    script = f"""
Breaking news.

{title}.

This is happening right now.

Stay updated for more.
"""

    filename = f"news_{i}_{datetime.now().strftime('%H%M%S')}"
    audio = f"{OUTPUT_DIR}/{filename}.mp3"
    video = f"{OUTPUT_DIR}/{filename}.mp4"

    # Generate voice
    engine.save_to_file(script, audio)
    engine.runAndWait()

    # Check if bg video exists
    if os.path.exists(BG_VIDEO):
        input_video = f"-stream_loop -1 -i {BG_VIDEO}"
    else:
        input_video = "-f lavfi -i color=c=black:s=1080x1920:d=15"

    cmd = f"""
    ffmpeg -y {input_video} -i {audio} \
    -vf "scale=1080:1920,
    drawbox=y=0:color=red@0.8:width=iw:height=150:t=fill,
    drawtext=text='BREAKING NEWS':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=40,
    drawtext=text='{title}':fontcolor=white:fontsize=42:x=60:y=1400" \
    -shortest -pix_fmt yuv420p {video}
    """

    subprocess.call(cmd, shell=True)

print("DONE: Videos created")
