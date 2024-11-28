import ffmpeg
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip


def speedup_audio(audio_input, speed_factor, output_audio):
    # ffmpeg -i {utils.temp_mp3_path} -af atempo=1.35 -y {utils.audio_mp3_path}
     audio_input_stream = ffmpeg.input(audio_input)
     stream = ffmpeg.output(audio_input_stream, output_audio, af=f"atempo={speed_factor}")
     ffmpeg.run(stream, overwrite_output=True, quiet=True)


def create_temp_video(video_input, audio_input, output_video):
    # Load the video and audio
    video = VideoFileClip(video_input)
    audio = AudioFileClip(audio_input)

    # Get the shorter duration
    shortest_duration = min(video.duration, audio.duration)

    # Trim both video and audio to the shortest duration
    video = video.subclip(0, shortest_duration)
    audio = audio.subclip(0, shortest_duration)

    # Set the audio to the video
    video_with_audio = video.set_audio(audio)

    # Save the resulting video
    video_with_audio.write_videofile(output_video, codec="libx264", audio_codec="aac",)

def create_temp_video_old(video_input, audio_input, output_video):
    result = subprocess.run(f"ffmpeg -i {video_input} -i {audio_input} -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -y {output_video}".split())
    if result.returncode != 0:
        print("Failed to merge audio and video.")
        print(result.stderr)
        return False
    else:
        return True

def create_final_video(video_input, srt_file, output_video):
    print("Adding the subtitles to the video...")
    video_input_stream = ffmpeg.input(video_input)
    stream = ffmpeg.output(video_input_stream, output_video, vf=f"subtitles={srt_file}:force_style='Alignment=10'").run(overwrite_output=True, quiet=True)