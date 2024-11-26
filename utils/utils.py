from os import makedirs, path, listdir
import random


TEMP_FOLDER = "temp"
OUTPUT_DIR = "out"
BACKGROUND_VIDEOS = "bg_vids"
audio_file_name = "final"


if not path.exists(OUTPUT_DIR):
    makedirs(OUTPUT_DIR)

if not path.exists(BACKGROUND_VIDEOS):
    makedirs(BACKGROUND_VIDEOS)

if not path.exists(TEMP_FOLDER):
    makedirs(TEMP_FOLDER)


input_file_path = path.join(TEMP_FOLDER, "input.txt")

temp_mp3_path = path.join(TEMP_FOLDER, "temp.mp3")
audio_mp3_path = path.join(TEMP_FOLDER, audio_file_name + ".mp3")

final_srt_file = f"{TEMP_FOLDER}/{audio_file_name}.srt"

def return_random_video():
    videos = listdir(BACKGROUND_VIDEOS)
    if not videos:
        print("No videos found in the output directory.")
        return None

    random_video = random.choice(videos)
    return path.join(BACKGROUND_VIDEOS, random_video)

partmp4_path = path.join(TEMP_FOLDER, "temp.mp4")
final_upload = path.join(OUTPUT_DIR, "upload.mp4")