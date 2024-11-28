import subprocess, shutil, os, time
from utils import redditreq, generate_subs, tts, variables, video, utils
import datetime

IPV4_ADRESS = "http://127.0.0.1:9090"  # Replace with your IPv4 address
HOURS = 1 # How many hours between posts

SUCESS = True
FAILED = False

def main():
    utils.setup_directories()

    print("Making a request to reddit...")
    random_post = redditreq.get_random_post_text()
    print("Title:", random_post["title"])
    print("Subreddit:", random_post["sub"])
    print("post_id:", random_post["id"])


    body = random_post["body"].replace(" ", "").replace("‘", "'").replace("’", "'").replace("“", "\"").replace("”", "\"")
    with open(variables.input_file_path, "w") as file:
        print("Writing to output.txt...")
        file.write(body)

    if not os.path.exists(variables.input_file_path):
        print(f"{variables.input_file_path} not found")
        return FAILED

    tts.text_to_speech(variables.input_file_path, variables.temp_mp3_path, IPV4_ADRESS)

    if not os.path.exists(variables.temp_mp3_path):
        print("input.mp3 not found")
        return FAILED

    print("Speeding up the audio track...")
    video.speedup_audio(variables.temp_mp3_path, 1.35, variables.audio_mp3_path)
    if not os.path.exists(variables.audio_mp3_path):
        return FAILED

    os.remove(variables.temp_mp3_path)

    print("Adding the audio track to the video...")

    # subprocess.run(f"ffmpeg -i {utils.return_random_video()} -i {variables.audio_mp3_path} -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -y {variables.partmp4_path}".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    video.create_temp_video(utils.return_random_video(), variables.audio_mp3_path, variables.partmp4_path)
    # result = video.create_temp_video(utils.return_random_video(), variables.audio_mp3_path, variables.partmp4_path)
    # if not result:
    #     return FAILED

    print("Generating subtitles...")
    generate_subs.run(variables.audio_mp3_path, variables.final_srt_file)

    video.create_final_video(variables.partmp4_path, variables.final_srt_file, variables.final_upload)

    session_id = "0b9e6d830a112c460718ed5dc2b478d8"
    file = variables.final_upload
    title = random_post["title"]
    tags = ["scary", "spooky", "scarystories", "fyp"]
    users = ["poweredbyreddit"]

    # Publish the video
    # TODO: Add your own upload function here

    return SUCESS

if __name__ == "__main__":
    while True:
        failed = False
        while not failed:
            failed = main()
        print("Sucessfully uploaded video. Waiting...")
        time.sleep(HOURS * 60 * 60)