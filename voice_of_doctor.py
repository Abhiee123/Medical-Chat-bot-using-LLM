# Import necessary modules
import os
import subprocess
import platform
from gtts import gTTS
from pydub import AudioSegment  # Ensure you install pydub: `pip install pydub`

# Function for gTTS Text-to-Speech
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    # Convert MP3 to WAV if using Windows SoundPlayer
    if platform.system() == "Windows":
        wav_output = output_filepath.replace(".mp3", ".wav")
        AudioSegment.from_mp3(output_filepath).export(wav_output, format="wav")
        output_filepath = wav_output

    # Play the audio
    play_audio(output_filepath)

# Function to Play Audio Based on OS
def play_audio(output_filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Test GTTS (Google TTS)
text_to_speech_with_gtts("Hi this is Abhi from Bengaluru!!!", "gtts_testing_autoplay.mp3")

# Replacing ElevenLabs with GTTS
text_to_speech_with_gtts("Hi this is Abhi, autoplay testing!", "gtts_testing_autoplay2.mp3")
