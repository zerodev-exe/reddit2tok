import random
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import *
import os
from rich.console import Console
from utils.utils import *
from utils import generate_subs

MAX_VIDEO_LENGTH = 5 * 60  # Maximum video length in seconds (5 minutes)
MIN_VIDEO_LENGTH = 0.5*60  # Minimum video length in seconds (30 seconds)

console = Console()

def process_video(audio_input, audio_output, video_input, srt_file, output_video, speed_factor):
    # Step 1: Speed up the audio
    print_step("Speeding up the audio track...")
    audio = AudioFileClip(audio_input)
    sped_up_audio = audio.fx(vfx.speedx, factor=speed_factor)
    sped_up_audio.write_audiofile(audio_output)
    audio.close()

    os.remove(audio_input)

    video = VideoFileClip(video_input)
    audio = AudioFileClip(audio_output)

    if audio.duration > MAX_VIDEO_LENGTH or audio.duration < MIN_VIDEO_LENGTH:
        error_print(f"The video exceeded either the max video length which is {MAX_VIDEO_LENGTH} secs or exceeded the minimum video length which is {MIN_VIDEO_LENGTH} secs")
        audio.close()
        video.close()
        return False

    print_step("Generating subtitles...")
    if not generate_subs.run(audio_output, srt_file):
        return False
    if not os.path.exists(srt_file) or os.path.getsize(srt_file) == 0:
        error_print(f"Subtitle file {srt_file} does not exist or is empty.")
        return False

    shortest_duration = min(video.duration, audio.duration)
    starting_frame = random.choice([0.0, (video.duration - shortest_duration)])
    video = video.subclip(starting_frame, starting_frame + shortest_duration)
    audio = audio.subclip(0, shortest_duration)

    video_with_audio = video.set_audio(audio).speedx(factor=1)

    # Step 3: Load the subtitles
    if not os.path.exists(srt_file) or os.path.getsize(srt_file) == 0:
        error_print(f"Subtitle file {srt_file} does not exist or is empty.")
        return False

    def subtitle_generator(txt):
        from moviepy.video.VideoClip import TextClip
        return TextClip(txt, fontsize=100, color='white', method='caption', stroke_color="black")

    subtitles = SubtitlesClip(srt_file, subtitle_generator)

    final_video = CompositeVideoClip([video_with_audio, subtitles.set_position(('center', 'center'))])

    if not os.path.exists(OUTPUT_DIR):
        makedirs(OUTPUT_DIR)

    # Write the final output video
    final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")
    success_print("Video creation complete!")
    return True

def upload(video_path, caption):
    from tiktok_uploader.upload import upload_video
    upload_video(sessionid=os.getenv("TIKTOK_SESSION_ID"), filename=video_path, description=caption, browser='firefox')