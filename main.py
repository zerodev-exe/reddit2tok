import subprocess
import os
import time
from utils import redditreq, generate_subs, utils, tts, video
from tiktok_uploader import tiktok, Config

IPV4_ADRESS = "http://127.0.0.1:9090"  # Replace with your IPv4 address
HOURS = 1 # How many hours between posts

SUCESS = True
FAILED = False

def main():
    print("Making a request to reddit...")
    random_post = redditreq.get_random_post_text()
    print("Title:", random_post["title"])
    body = random_post["body"].replace(" ", "").replace("‘", "'").replace("’", "'").replace("“", "\"").replace("”", "\"")
    with open(utils.input_file_path, "w") as file:
        print("Writing to output.txt...")
        file.write(body)

    if not os.path.exists(utils.input_file_path):
        print("output.txt not found")
        return FAILED

    print("Creating the audio track...")
    tts.text_to_speech(utils.input_file_path, utils.temp_mp3_path, IPV4_ADRESS)

    if not os.path.exists(utils.temp_mp3_path):
        print("input.mp3 not found")
        return FAILED

    result = subprocess.run(f"ffmpeg -i {utils.temp_mp3_path} -af atempo=1.35 -y {utils.audio_mp3_path}".split(), check=True)
    if result.returncode != 0:
        print("Failed to speed up audio.")
        print(result.stderr)
        return FAILED

    if not os.path.exists(utils.audio_mp3_path):
        return FAILED

    result = subprocess.run(f"ffmpeg -i {utils.return_random_video()} -i {utils.audio_mp3_path} -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -y {utils.partmp4_path}".split())
    if result.returncode != 0:
        print("Failed to merge audio and video.")
        print(result.stderr)
        return FAILED

    print("Generating subtitles...")
    subprocess.run(f"whisper {utils.audio_mp3_path} --model turbo --output_format srt --output_dir {utils.TEMP_FOLDER} --language English --max_words_per_line 3 --max_line_width 15 --word_timestamps True".split())

    result = subprocess.run(f"ffmpeg -i {utils.partmp4_path} -vf 'iw*0.25:ih*1' -vf subtitles='{utils.final_srt_file}':force_style='Alignment=10' -y {utils.final_upload}".split())
    if result.returncode != 0:
        print(result.stderr)
        return FAILED

    tiktok.upload_video("user", "upload.mp4",  random_post["title"])
    return SUCESS

if __name__ == "__main__":
    _ = Config.load("./config.txt")
    while True:
        failed = False
        while not failed:
            failed = main()
        print("Sucessfully uploaded video. Waiting...")
        time.sleep(HOURS * 60 * 60)