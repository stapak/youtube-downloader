import requests

def download_video(url, file_name):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("Download complete!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    video_url = input("Enter the direct video URL: ")
    file_name = input("Enter the desired file name (with extension, e.g., video.mp4): ")
    download_video(video_url, file_name)
