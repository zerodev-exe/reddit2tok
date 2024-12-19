import os
from utils import redditreq, generate_subs, tts, variables, video, utils
from utils.utils import *
from moviepy.editor import AudioFileClip
from dotenv import load_dotenv

load_dotenv()

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
    if len(random_post["body"]) > 8000:
        error_print("Post body is too long, skipping...")
        return False
    if random_post["body"] == " " or random_post["body"] == "":
        error_print("Post body is empty, skipping...")
        return FAILED
    body = utils.sanitize_text(random_post["body"])

    with open(variables.input_file_path, "w", encoding="utf-8") as file:
        print(f"Writing to {variables.input_file_path}...")
        file.write(body)
        file.write("If you liked this video, please like, comment and give me a follow!")
    if not os.path.exists(variables.input_file_path):
        error_print(f"{variables.input_file_path} not found")
        return FAILED

    print_step("Creating the audio track...")
    tts.text_to_speech(variables.input_file_path, variables.temp_mp3_path, IPV4_ADRESS)

    # Check if the file was created
    if not os.path.exists(variables.temp_mp3_path):
        error_print(f"{variables.temp_mp3_path} not found after TTS call")
        return FAILED

    # print_step("Adding the audio track to the video...")
    # video.create_temp_video(utils.return_random_video(), variables.audio_mp3_path, variables.partmp4_path)

    print_step("Adding subtitles to the video...")
    video_name = random_post["title"].replace("?", "").replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_").replace("\n", "").replace("\r", "")

    output_file = f"out/{video_name}-{random_post['sub']}.mp4"
    # video.create_final_video(variables.partmp4_path, variables.final_srt_file, output_video=output_file)

    if not video.process_video(audio_input=temp_mp3_path, audio_output=audio_mp3_path, video_input=return_random_video(), srt_file=final_srt_file, output_video=output_file, speed_factor=1.35):
        return False


    session_id = os.getenv("TIKTOK_SESSION_ID")
    title = random_post["title"]
    if random_post["sub"] == "nosleep":
        tags = ["scary", "spooky", "scarystories", "fyp"]
    elif random_post["sub"] == "confession":
        tags = ["confession", "confessions", "fyp"]

    # Publish the video
    # TODO: Add your own upload function here
    
    print(" ".join(tags))
    
    # video.upload(output_file, title+" ".join(tags))

    
    utils.cleanup()
    
    return SUCESS

if __name__ == "__main__":
    for i in range(5):
    # while True:
        succeeded = False
        while not succeeded:
            succeeded = main()
    success_print(f"Sucessfully uploaded video. Waiting... {HOURS} hours")