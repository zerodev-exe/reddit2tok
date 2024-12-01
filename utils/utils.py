import shutil
import re
import random
from os import makedirs, path, listdir
from utils.variables import *
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_step(text) -> None:
    """Prints a rich info message."""

    panel = Panel(Text(text, justify="left"))
    console.print(panel)


def setup_directories():
    if not os.path.exists(OUTPUT_DIR):
        makedirs(OUTPUT_DIR)

    if not os.path.exists(BACKGROUND_VIDEOS):
        makedirs(BACKGROUND_VIDEOS)

    if not os.path.exists(TEMP_FOLDER):
        makedirs(TEMP_FOLDER)

def cleanup():
    shutil.rmtree(OUTPUT_DIR)
    shutil.rmtree(TEMP_FOLDER)
def return_random_video():
    videos = listdir(BACKGROUND_VIDEOS)
    if not videos:
        print("No videos found in the output directory.")
        return None

    random_video = random.choice(videos)
    return os.path.join(BACKGROUND_VIDEOS, random_video)

def sanitize_text(text: str) -> str:
    r"""Sanitizes the text for tts.
        What gets removed:
     - following characters`^_~@!&;#:-%“”‘"%*/{}[]()\|<>?=+`
     - any http or https links

    Args:
        text (str): Text to be sanitized

    Returns:
        str: Sanitized text
    """

    # remove any urls from the text
    regex_urls = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

    result = re.sub(regex_urls, " ", text)

    # note: not removing apostrophes
    regex_expr = r"\s['|’]|['|’]\s|[\^_~@!&;#:\-%—“”‘\"%\*/{}\[\]\(\)\\|<>=+]"
    result = re.sub(regex_expr, " ", result)
    result = result.replace("+", "plus").replace("&", "and")
    result = result.encode('utf8', errors='replace').decode("utf-8")

    # remove extra whitespace
    return " ".join(result.split())
