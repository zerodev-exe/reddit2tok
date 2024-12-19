import os
import random
import string

TEMP_FOLDER = "temp"
OUTPUT_DIR = "out"
BACKGROUND_VIDEOS = "bg_vids"
audio_file_name = "final"

input_file_path = os.path.join(TEMP_FOLDER, "input.txt")

temp_mp3_path = os.path.join(TEMP_FOLDER, "temp.mp3")
audio_mp3_path = os.path.join(TEMP_FOLDER, audio_file_name + ".mp3")

final_srt_file = f"{TEMP_FOLDER}/{audio_file_name}.srt"

partmp4_path = os.path.join(TEMP_FOLDER, "temp.mp4")

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits  # You can add punctuation if needed
    return ''.join(random.choice(letters) for i in range(length))