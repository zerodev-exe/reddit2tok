import shutil
import random
from os import makedirs, path, listdir
from utils.variables import *


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
