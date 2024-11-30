import subprocess, shutil, os, time

from utils import redditreq, generate_subs, tts, variables, video, utils
import datetime
from utils.utils import *

IPV4_ADRESS = "http://localhost:9090"  # Replace with your IPv4 address
HOURS = 1 # How many hours between posts

SUCESS = True
FAILED = False

def main():
    utils.setup_directories()

    print_step("Making a request to reddit...")
    random_post = redditreq.get_random_post_text()
    print("Title:", random_post["title"])
    print("Subreddit:", random_post["sub"])
    print("Post Link:", random_post["url"])
    if random_post["body"] == "":
        print("Post body is empty, skipping...")
        return FAILED

    body = utils.sanitize_text(random_post["body"])
    with open(variables.input_file_path, "w") as file:
        print("Writing to output.txt...")
        file.write(body)
        file.write("If you liked this video, please like, comment and give me a follow!")
    if not os.path.exists(variables.input_file_path):
        print(f"{variables.input_file_path} not found")
        return FAILED

    tts.text_to_speech(variables.input_file_path, variables.temp_mp3_path, IPV4_ADRESS)
    if not os.path.exists(variables.temp_mp3_path):
        print("input.mp3 not found")
        return FAILED
    else:
        os.remove(variables.input_file_path)

    print("Speeding up the audio track...")
    video.speedup_audio(variables.temp_mp3_path, 1.35, variables.audio_mp3_path)
    if not os.path.exists(variables.audio_mp3_path):
        print("Couldn't speed up the audio track")
        return FAILED

    os.remove(variables.temp_mp3_path) # Deleting the temporary mp3 file because if we don't it's going to 100% fill up the disk

    print("Adding the audio track to the video...")
    video.create_temp_video(utils.return_random_video(), variables.audio_mp3_path, variables.partmp4_path)

    print_step("Generating subtitles...")
    generate_subs.run(variables.audio_mp3_path, variables.final_srt_file)
    if not os.path.exists(variables.final_srt_file):
        return FAILED

    print_step("Adding subtitles to the video...")
    # video.create_final_video(variables.partmp4_path, variables.final_srt_file, variables.final_upload)
    video.create_final_video(variables.partmp4_path, variables.final_srt_file, "out/"+random_post["title"]+".mp4")

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
