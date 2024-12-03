import subprocess
import random
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import *
import os
from dotenv import load_dotenv

load_dotenv()

def speedup_audio_moviepy(audio_input, speed_factor, output_audio):
    # Load the audio file
    audio = AudioFileClip(audio_input)
    
    # Speed up the audio
    sped_up_audio = audio.fx(vfx.speedx, factor=speed_factor)
    
    # Write the sped-up audio to a file
    sped_up_audio.write_audiofile(output_audio)
    print("Audio speed-up complete!")

def create_temp_video(video_input, audio_input, output_video):
    # Load the video and audio
    video = VideoFileClip(video_input)
    audio = AudioFileClip(audio_input)

    # Get the shorter duration
    shortest_duration = min(video.duration, audio.duration)

    starting_frame = random.choice([0.0, (video.duration - shortest_duration)])

    # Trim both video and audio to the shortest duration
    video = video.subclip(starting_frame,  starting_frame + shortest_duration)
    audio = audio.subclip(0, shortest_duration)

    # Set the audio to the video
    video_with_audio = video.set_audio(audio).speedx(factor=1)

    # Save the resulting video
    video_with_audio.write_videofile(output_video, codec="libx264", audio_codec="aac",)

def create_final_video(video_input, srt_file, output_video):
    # Check if the SRT file exists and is not empty
    if not os.path.exists(srt_file) or os.path.getsize(srt_file) == 0:
        print(f"Subtitle file {srt_file} does not exist or is empty.")
        return  # Handle this case appropriately

    # Load the video
    video = VideoFileClip(video_input)
    
    # Load the subtitles
    def subtitle_generator(txt):  # Function to style subtitles
        from moviepy.video.VideoClip import TextClip
        return TextClip(txt, fontsize=100, color='white', method='caption', stroke_color="black")
    
    subtitles = SubtitlesClip(srt_file, subtitle_generator)
    
    # Overlay subtitles on the video
    final_video = CompositeVideoClip([video, subtitles.set_position(('center', 'center'))])
    
    # Write the output video
    final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")
    print("Video creation complete!")