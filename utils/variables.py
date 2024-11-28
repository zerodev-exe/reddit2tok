import os

TEMP_FOLDER = "temp"
OUTPUT_DIR = "out"
BACKGROUND_VIDEOS = "bg_vids"
audio_file_name = "final"

input_file_path = os.path.join(TEMP_FOLDER, "input.txt")

temp_mp3_path = os.path.join(TEMP_FOLDER, "temp.mp3")
audio_mp3_path = os.path.join(TEMP_FOLDER, audio_file_name + ".mp3")

final_srt_file = f"{TEMP_FOLDER}/{audio_file_name}.srt"

partmp4_path = os.path.join(TEMP_FOLDER, "temp.mp4")
final_upload = os.path.join(OUTPUT_DIR, "upload.mp4")