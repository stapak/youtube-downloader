from pytubefix import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os
from os import system,name
import time

import threading
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def download_video(url,cleanup):
    try:
        try:
            yt = YouTube(url)
        except Exception as e:
            print("URL is not reachable , video might be removed or can be only for members.")
            return None
        print(f"Title: {yt.title}")
        # List available streams
        video_streams = yt.streams.filter(adaptive=True).order_by('resolution')
        for i, stream in enumerate(video_streams, 1):
            print(f"{i}. {stream.resolution} - {stream.mime_type}")
        # Choose the desired quality
        try:
            choice = int(input("Enter the number corresponding to the desired resolution: ")) - 1
        except Exception as e:
            print("Enter a valid choice")
            return None
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
        return None
    
    video_clip.close()
    audio_clip.close()
    if cleanup:
        os.remove(video_path)
        os.remove(audio_path)
    return None

    
def download_audio(url):
    try:
        try:
            yt = YouTube(url)
        except Exception as e:
            print("URL is not reachable , video might be removed or can be only for members.")
            return None
        print(f"Title: {yt.title}")
        audio_streams = yt.streams.filter(only_audio=True) 
        for i, stream in enumerate(audio_streams, 1): 
            print(f"{i}. {stream.mime_type} - {stream.abr} - {stream.audio_codec}")
        try:
            choice = int(input("Enter the number corresponding to the desired resolution of audio: ")) - 1
            audio_stream = audio_streams[choice]
        except Exception as e:
            print("Enter a valid choice")
            return None
        audio_path=audio_stream.download(filename=f"{yt.title}")
        print("audio download complete")
        return None
    except Exception as e:
        print("Error ouccured:",e)
        return None

def launch_app():
    clear()
    print("\t\tYoutube Video Downloader")
    print("Note:")
    print("*As downloader combines audio and video in your device video download speed might be dependent on your internet and cpu.")
    try:
        choice=int(input("1.donwload video\n2.download audio\n3.to quit \nEnter your choice for action:"))
    except Exception as e:
        clear()
        print("Invalid input given !!!")
        print("Enter a valid input in:")
        i=3
        while (i>0):
            print(i)
            time.sleep(1)
            i-=1
        launch_app()
    match choice:
        case 1:
            url = input("Enter the YouTube video URL: ")
            try:
                cleanup=int(input("Do you want to delete raw files1 of download(0/1):"))
            except Exception as e:
                print("enter a valid choice")
                launch_app()
            t1=threading.Thread(target=download_video,args=(url,cleanup))
            t1.start()
            t1.join()
            launch_app()
        case 2:
            url = input("Enter the YouTube video URL: ")
            t1=threading.Thread(target=download_audio,args=(url))
            t1.start()
            t1.join()
            launch_app()
        case 3:
            exit()
        case _:
            print("enter a valid choice !!!")
            launch_app()


launch_app()
