import os
import shutil
from yt_dlp import YoutubeDL

def download_youtube_video(video_url):
    output_dir = 'static/uploads'

    # Step 1: Clear existing files
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        os.makedirs(output_dir)

    # Step 2: Download video with audio (ensure proper format)
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'cookiefile': 'youtube_cookies.txt',
        'quiet': False,
        'noplaylist': True,
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # force final format
            }
        ]
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# 🧪 Example usage
# download_youtube_video("https://www.youtube.com/watch?v=AMfuIWDUDHg")

