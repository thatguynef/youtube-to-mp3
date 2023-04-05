from pytube import YouTube
from moviepy.editor import *
import os
import re

# List of YouTube links
links = [
    "https://youtu.be/xKftq1aBqNA",
    "https://youtu.be/CfqbzWdQOVw",
    "https://youtu.be/GADD101GPvs",
    "https://youtu.be/IMV_3Uq5gu8",
    "https://youtu.be/xj-bieOC6zY",
    "https://youtu.be/_S9FbYxTxi4",
    "https://youtu.be/XlpQikimL40",
    "https://youtu.be/GYP2_LWk2zc",
    "https://youtu.be/L_FW2QK3M7w",
    "https://youtu.be/gKgqtQExQxA",
    "https://youtu.be/z7L6XzjcgEk",
    "https://youtu.be/0oj8QHiQbY0",
    "https://youtu.be/Zrf4iMgqfQo"
]

# List to store audio clips
audio_clips = []

for link in links:
    # Check that the link is a valid YouTube link
    if not re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', link):
        print(f"Error: Invalid YouTube link: {link}")
        continue

    # Extract the video ID from the link
    video_id = None
    if "/watch?v=" in link:
        video_id = link.split("/watch?v=")[1][:11]
    elif "/v/" in link:
        video_id = link.split("/v/")[1][:11]
    elif "youtu.be/" in link:
        video_id = link.split("youtu.be/")[1][:11]

    if not video_id:
        print(f"Error: Unable to extract video ID from link: {link}")
        continue

    # Create a YouTube object and extract the audio stream
    try:
        yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio stream as a .mp4 file
        audio_file = audio_stream.download()

        # Use moviepy to convert the .mp4 file to a .mp3 file
        audio_clip = AudioFileClip(audio_file)
        audio_clips.append(audio_clip)  # Add the audio clip to the list

        # Remove the original .mp4 file
        os.remove(audio_file)

        print(f"Conversion complete for {link}!")
    except Exception as e:
        print(f"Error for {link}:", e)

# Merge all audio clips into one
merged_audio = concatenate_audioclips(audio_clips)
merged_audio.write_audiofile("merged_audio.mp3")

print("Merging complete!")
