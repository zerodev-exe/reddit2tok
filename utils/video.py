import ffmpeg
from utils.utils import *

def create_final_video():
    video_input_stream = ffmpeg.input(partmp4_path, vf=f"'iw*0.25:ih*1' ")
    stream = ffmpeg.output(video_input_stream ,final_upload, vf=f"subtitles={final_srt_file}:force_style='Alignment=10'", )
    ffmpeg.run(stream, overwrite_output=True)