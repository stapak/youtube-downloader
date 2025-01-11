from pytubefix import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os

import threading

def download_video(url,cleanup):
    try:
        yt = YouTube(url)
        print(f"Title: {yt.title}")
        # List available streams
        video_streams = yt.streams.filter(adaptive=True).order_by('resolution')
        for i, stream in enumerate(video_streams, 1):
            print(f"{i}. {stream.resolution} - {stream.mime_type}")
        # Choose the desired quality
        choice = int(input("Enter the number corresponding to the desired resolution: ")) - 1
        video_stream = video_streams[choice]
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).first()

        # Download audio stream
        print(f"Downloading video: {video_stream.resolution}") 
        video_path = video_stream.download(filename='video')
        print("Video downlaod completed") 
        print("Downloading audio") 
        audio_path = audio_stream.download(filename='audio')
        print("Download completed!")

        print("Combining video and audio")
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path) 
        final_clip = video_clip.set_audio(audio_clip)
        try:
            final_clip.write_videofile(f"{yt.title}.mp4", codec='libx264 -c:v h264_nvenc', audio_codec='aac')
        except Exception as e:
            print("method 2",e)
            #final_clip.write_videofile(f"{yt.title}.mp4", codec='libx264', audio_codec='aac')
        print("Download and combination completed!")
    except Exception as e:
        print("Error detected \nError is:",e)
    
    video_clip.close()
    audio_clip.close()
    if cleanup:
        os.remove(video_path)
        os.remove(audio_path)

    
def download_audio(url,cleanup):
    yt = YouTube(url)
    print(f"Title: {yt.title}")
    audio_streams = yt.streams.filter(only_audio=True) 
    for i, stream in enumerate(audio_streams, 1): 
        print(f"{i}. {stream.mime_type} - {stream.abr} - {stream.audio_codec}")
    try:
        choice = int(input("Enter the number corresponding to the desired resolution of audio: ")) - 1
        audio_stream = audio_streams[choice]
    except Exception as e:
        print("Enter a valid choice")
    audio_path=audio_stream.download(filename=input("Enter file name:"))
    print("audio download complete")
    if cleanup:
        os.remove(audio_path)


choice=int(input("1.donwload video\n2.download audio\nEnter your choice for action:"))
match choice:
    case 1:
        url = input("Enter the YouTube video URL: ")
        cleanup=int(input("Do you want a cleanup after the completion of download(0/1):"))
        #download_video(url,cleanup)
        t1=threading.Thread(target=download_video,args=(url,cleanup))
        t1.start()
    case 2:
        url = input("Enter the YouTube video URL: ")
        cleanup=int(input("Do you want a cleanup after the completion of download(0/1):"))
        download_audio(url,cleanup)