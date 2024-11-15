import subprocess
import os
import time
import random
import string
import redditreq
from TiktokAutoUploader.tiktok_uploader import tiktok, Config

IPV4_ADRESS = "localhost"  # Replace with your IPv4 address

def main():
    random_post = redditreq.get_random_post_text()
    print("Title:", random_post["title"])
    print("Body:", random_post["body"])
    body = random_post["body"].replace(" ", "").replace("’", "'")
    with open("output.txt", "w") as file:
        file.write(body)
    subprocess.run(f"curl -X POST --data-binary @output.txt -o audio.mp3 {IPV4_ADRESS}:9090/api/tts".split())
    subprocess.run("ffmpeg -i minecraft.mp4 -i audio.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -y upload-part.mp4".split())
    subprocess.run("whisper audio.mp3 --model turbo --language English --max_words_per_line 3 --max_line_width 15 --word_timestamps True".split())
    # ffmpeg -i minecraft.mp4 -vf "subtitles=output.srt:force_style='Alignment=10',zoompan=z='if(lte(in,25),1+0.02*in,1+0.02*(50-in))':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'" -y upload.mp4

    subprocess.run("ffmpeg -i upload-part.mp4 -vf 'iw*0.25:ih*1' -vf subtitles=audio.srt:force_style='Alignment=10' -y out/upload.mp4".split())

    # Cleaning up
    os.remove("output.txt")
    os.remove("audio.*")
    os.remove("upload-part.mp4")
    

    # subprocess.run(f"python TiktokAutoUploader\cli.py upload -u poweredbyreddit -t {random_post["title"]} -v upload.mp4".split())
    _ = Config.load("./TiktokAutoUploader/config.txt")
    tiktok.upload_video("poweredbyreddit", "upload.mp4",  random_post["title"])

if __name__ == "__main__":
    main()