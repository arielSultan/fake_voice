import os
from yt_dlp import YoutubeDL
from datetime import datetime


def download_audio_from_playlist(playlist_url,download_directory):
    os.makedirs(download_directory, exist_ok=True)
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(
            download_directory, f"audio_{current_datetime}_%(autonumber)s.%(ext)s"
        ),
        "ignoreerrors": True, 
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
       ydl.download([playlist_url])


def main():
    playlist_url = "https://www.youtube.com/watch?v=sqdXkSbszME&list=PLJS4Xanymi70SQPc1J1TQXBzr0qQC4eCT"
    dir=r"C:\dataset\others"
    download_audio_from_playlist(playlist_url,dir)


if __name__ == "__main__":
    main()