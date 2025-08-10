import yt_dlp

def download_youtube_video_yt_dlp(url, output_path="data/videos/interview.mp4"):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': output_path,
        'quiet': False,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"Downloaded video saved to {output_path}")

if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()
    download_youtube_video_yt_dlp(url)
