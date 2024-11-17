import subprocess
import os
import time
import random
import string
import redditreq
from tiktok_uploader import tiktok, Config

IPV4_ADRESS = "localhost"  # Replace with your IPv4 address

def main():
    random_post = redditreq.get_random_post_text()
    print("Title:", random_post["title"])
    body = random_post["body"].replace(" ", "").replace("’", "'").replace("“", "\"").replace("”", "\"")
    with open("output.txt", "w") as file:
        file.write(body)
    subprocess.run(f"curl -X POST --data-binary @output.txt -o audio.mp3 {IPV4_ADRESS}:9090/api/tts".split())

    result = subprocess.run("ffmpeg -i base/minecraft-20min.mp4 -i audio.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -y upload-part.mp4".split())
    if result.returncode != 0:
        print(result.stderr)
        return True

    

    subprocess.run("whisper audio.mp3 --model turbo --language English --max_words_per_line 3 --max_line_width 15 --word_timestamps True".split())

    # Adding the subtitles
    subprocess.run("ffmpeg -i upload-part.mp4 -vf 'iw*0.25:ih*1' -vf subtitles=audio.srt:force_style='Alignment=10' -y out/upload.mp4".split())

    # Cleaning up
    os.remove("output.txt")
    os.remove("audio.json")
    os.remove("audio.mp3")
    os.remove("audio.srt")
    os.remove("audio.tsv")
    os.remove("audio.txt")
    os.remove("audio.vtt")
    os.remove("upload-part.mp4")

    # subprocess.run(f"python TiktokAutoUploader\cli.py upload -u poweredbyreddit -t {random_post["title"]} -v upload.mp4".split())
    tiktok.upload_video("poweredbyreddit", "upload.mp4",  random_post["title"])
    return False

if __name__ == "__main__":
    _ = Config.load("./TiktokAutoUploader/config.txt")
    fail = True
    while True:
        fail = main()