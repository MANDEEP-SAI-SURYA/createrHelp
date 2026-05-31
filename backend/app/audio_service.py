import os
import uuid
import yt_dlp

DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_audio(url):

    file_id = str(uuid.uuid4())

    output = os.path.join(
        DOWNLOAD_DIR,
        file_id
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output + ".%(ext)s",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    files = os.listdir(DOWNLOAD_DIR)

    for f in files:
        if file_id in f:
            return os.path.join(
                DOWNLOAD_DIR,
                f
            )

    return None