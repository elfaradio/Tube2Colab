import yt_dlp
import re
import os
import requests

PLAYLIST_URL = "https://youtube.com/playlist?list=PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH&si=EDQcFERQ2j-y3xFX"

OUTPUT_DIR = r"G:\ALL_Colab"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ydl_opts = {
    "quiet": True,
    "extract_flat": False,
    "skip_download": True,
    "ignoreerrors": True,
    "no_warnings": True
}

all_colab_links = []

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    playlist_info = ydl.extract_info(PLAYLIST_URL, download=False)

    for video in playlist_info.get("entries", []):

        if not video:
            continue

        if video.get("availability") not in [None, "public"]:
            continue

        title = video.get("title", "Untitled")
        description = video.get("description") or ""

        links = re.findall(
            r'https://colab\.research\.google\.com/[^\s]+',
            description
        )

        for link in links:
            all_colab_links.append({
                "title": title,
                "link": link.strip()
            })

seen = set()
unique = []

for item in all_colab_links:
    if item["link"] not in seen:
        seen.add(item["link"])
        unique.append(item)

all_colab_links = unique

links_file = os.path.join(OUTPUT_DIR, "all_colab_links.txt")

with open(links_file, "w", encoding="utf-8") as f:
    for item in all_colab_links:
        f.write(item["title"] + "\n")
        f.write(item["link"] + "\n\n")

download_count = 0

for item in all_colab_links:

    link = item["link"]
    title = re.sub(r'[\\/*?:"<>|]', "", item["title"])

    try:

        if "/github/" in link:

            raw = link.replace(
                "https://colab.research.google.com/github/",
                "https://raw.githubusercontent.com/"
            ).replace("/blob/", "/")

            r = requests.get(raw, timeout=20)

            if r.status_code == 200:
                path = os.path.join(OUTPUT_DIR, f"{title}.ipynb")
                with open(path, "wb") as f:
                    f.write(r.content)
                download_count += 1

        elif "/drive/" in link:

            match = re.search(r"/d/([a-zA-Z0-9_-]+)", link)

            if match:
                file_id = match.group(1)
                url = f"https://drive.google.com/uc?export=download&id={file_id}"

                r = requests.get(url, timeout=20)

                if r.status_code == 200:
                    path = os.path.join(OUTPUT_DIR, f"{title}.ipynb")
                    with open(path, "wb") as f:
                        f.write(r.content)
                    download_count += 1

    except:
        pass

print("Total links:", len(all_colab_links))
print("Downloaded:", download_count)
print("Saved in:", OUTPUT_DIR)
