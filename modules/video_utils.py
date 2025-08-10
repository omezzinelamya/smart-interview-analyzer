import os
import yt_dlp

def download_youtube_video(url, output_path="data/videos/interview.mp4"):
    try:
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return output_path
    except Exception as e:
        print(f"Download failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def save_uploaded_video(uploaded_file, output_path="data/videos/uploaded_interview.mp4"):
    try:
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
        with open(output_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return output_path
    except Exception as e:
        print(f"Error saving uploaded video: {e}")
        return None
