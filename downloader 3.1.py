import yt_dlp
def download_4k_video(url):
    ydl_opts = {
        'format': 'bestvideo[height=2160]+bestaudio/best[height=2160]',  # Select the best 4K video
        'outtmpl': '%(title)s.%(ext)s',  # Output file name format
        'merge_output_format': 'mp4',    # Format for merging video and audio
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
video_url=input("Enter the video url:")  # Replace with your video URL
download_4k_video(video_url)
