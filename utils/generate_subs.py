import math
from faster_whisper import WhisperModel
import os

num_cores = os.cpu_count()

def transcribe(audio):
    whisper_size = "turbo"
    model = WhisperModel(
        whisper_size,
        )
    segments, _ = model.transcribe(audio)

    segments = list(segments)
    for segment in segments:
        print("[%.2fs --> %.2fs] %s" %
              (segment.start, segment.end, segment.text))
    return segments

def split_segment_by_words_and_line_width(segment, max_words=3, max_line_width=15):
    words = segment.text.split()
    num_sub_segments = math.ceil(len(words) / max_words)
    duration_per_word = (segment.end - segment.start) / len(words)
    
    sub_segments = []
    for i in range(num_sub_segments):
        start_word_idx = i * max_words
        end_word_idx = min((i + 1) * max_words, len(words))
        sub_text = " ".join(words[start_word_idx:end_word_idx])

        # Split lines to meet the max_line_width constraint
        lines = []
        current_line = ""
        for word in sub_text.split():
            if len(current_line) + len(word) + 1 <= max_line_width:  # +1 for space
                current_line += (" " + word if current_line else word)
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        formatted_text = "\n".join(lines)

        sub_start_time = segment.start + start_word_idx * duration_per_word
        sub_end_time = segment.start + end_word_idx * duration_per_word
        
        sub_segments.append((sub_start_time, sub_end_time, formatted_text))
    
    return sub_segments

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    return formatted_time

def generate_subtitle_file(subtitle_file, segments, max_words=3, max_line_width=15):
    text = ""
    index = 0

    for segment in segments:
        sub_segments = split_segment_by_words_and_line_width(segment, max_words, max_line_width)
        for sub_segment in sub_segments:
            index += 1
            segment_start = format_time(sub_segment[0])
            segment_end = format_time(sub_segment[1])
            text += f"{str(index)}\n"
            text += f"{segment_start} --> {segment_end}\n"
            text += f"{sub_segment[2]}\n\n"
        
    with open(subtitle_file, "w") as f:
        f.write(text)

    return subtitle_file

def run(input_audio, srt_file):
    segments = transcribe(audio=input_audio)
    subtitle_file = generate_subtitle_file(subtitle_file=srt_file, segments=segments)

    print("Subtitle file generated:", subtitle_file)
