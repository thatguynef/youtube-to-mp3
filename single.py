from pytube import YouTube
from moviepy.editor import *
import re

# Prompt user to enter the YouTube link
link = input("Enter the YouTube link: ")
# link = ["https://youtu.be/GADD101GPvs"]

# Check that the link is a valid YouTube link
if not re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', link):
    print("Error: Invalid YouTube link")
    exit()

# Extract the video ID from the link
video_id = None
if "/watch?v=" in link:
    video_id = link.split("/watch?v=")[1][:11]
elif "/v/" in link:
    video_id = link.split("/v/")[1][:11]
elif "youtu.be/" in link:
    video_id = link.split("youtu.be/")[1][:11]

if not video_id:
    print("Error: Unable to extract video ID from link")
    exit()

# Create a YouTube object and extract the audio stream
try:
    yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Download the audio stream as a .mp4 file
    audio_file = audio_stream.download()

    # Use moviepy to convert the .mp4 file to a .mp3 file
    audio_clip = AudioFileClip(audio_file)
    audio_clip.write_audiofile(audio_file[:-4] + ".mp3")

    # Remove the original .mp4 file
    os.remove(audio_file)

    print("Conversion complete!")
except Exception as e:
    print("Error:", e)
