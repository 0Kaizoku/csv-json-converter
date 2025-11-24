from bs4 import BeautifulSoup
import csv
import json

# === CONFIG ===
HTML_FILE = "C:\\Users\\amine\\OneDrive\\Desktop\\exportcsv\\(540) Vidéos _J'aime_ - YouTube.html"
CSV_OUTPUT = "C:\\Users\\amine\\OneDrive\\Desktop\\exportcsv\\liked.csv"
JSON_OUTPUT = "C:\\Users\\amine\\OneDrive\\Desktop\\exportcsv\\liked.json"

# === FUNCTION TO EXTRACT YOUR PARAMETERS ===
def extract_video_items(soup):
    videos = []

    items = soup.find_all("ytd-playlist-video-renderer")

    for item in items:
        # Index
        index_tag = item.find(id="index")
        index = index_tag.get_text(strip=True) if index_tag else None

        # Title + URL
        title_tag = item.find("a", id="video-title")
        title = title_tag.get_text(strip=True) if title_tag else None
        link = title_tag.get("href") if title_tag else None

        # Channel
        channel_tag = item.select_one("#channel-name a")
        channel = channel_tag.get_text(strip=True) if channel_tag else None

        # Views + upload time
        info_tag = item.find(id="video-info")
        views = None
        upload_time = None
        if info_tag:
            spans = info_tag.find_all("span")
            if len(spans) > 0:
                views = spans[0].get_text(strip=True)
            if len(spans) > 1:
                upload_time = spans[-1].get_text(strip=True)

        # Thumbnail (safe)
        thumb_tag = item.find("img")
        thumbnail = thumb_tag.get("src") if thumb_tag else None

        # Duration (safe)
        duration_tag = item.select_one("ytd-thumbnail-overlay-time-status-renderer #text")
        duration = duration_tag.get_text(strip=True) if duration_tag else None

        videos.append({
            "index": index,
            "title": title,
            "url": link,
            "channel": channel,
            "views": views,
            "upload_time": upload_time,
            "duration": duration,
            "thumbnail": thumbnail
        })

    return videos



# === Load HTML ===
with open(HTML_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

videos = extract_video_items(soup)

# === Save CSV ===
with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=videos[0].keys())
    writer.writeheader()
    writer.writerows(videos)

# === Save JSON ===
with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(videos, f, indent=4, ensure_ascii=False)

print(f"Extracted {len(videos)} videos!")