import pyttsx3
import requests

def text_to_speech_old(input_file, output_file):
    try:
        # Read the content of the input file
        with open(input_file, 'r') as file:
            text = file.read()

        # Initialize the pyttsx3 engine
        engine = pyttsx3.init()

        # Configure the engine properties
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

        # Save the audio to an MP3 file
        engine.save_to_file(text, output_file)
        engine.runAndWait()

        print(f"Audio has been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def text_to_speech(input_file, output_file, ipv4_address):
    print("Creating the audio track...")
    """
    Sends a text file to a TTS API and saves the resulting speech to a file.

    Args:
        input_file (str): Path to the input text file.
        output_file (str): Path to save the output MP3 file.
        ipv4_address (str): IPv4 address and port of the TTS API server (e.g., 'http://127.0.0.1:9090').
    """
    url = f"{ipv4_address}/api/tts"
    
    try:
        with open(input_file, 'rb') as file:
            response = requests.post(url, data=file)
        
        if response.status_code == 200:
            with open(output_file, 'wb') as output:
                output.write(response.content)
            print(f"File saved to {output_file}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
