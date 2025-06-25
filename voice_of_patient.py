# If you don't use pipenv, uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# Step 1: Setup Audio Recorder (ffmpeg & portaudio)
import logging
import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
from io import BytesIO

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Ensure pydub finds FFmpeg
AudioSegment.converter = which("ffmpeg")  # Auto-detect FFmpeg

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Records audio from the microphone and saves it as a WAV file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert the recorded audio to a WAV file (required for recognition)
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="wav")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Save audio as WAV instead of MP3 for compatibility
audio_filepath = "patient_voice_test.wav"
record_audio(audio_filepath)

# Step 2: Setup Speech-to-Text (STT) Model for Transcription
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
stt_model = "whisper-large-v3"

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    """
    Transcribes an audio file using Groq's Whisper model.

    Args:
    stt_model (str): Name of the STT model.
    audio_filepath (str): Path to the audio file.
    GROQ_API_KEY (str): API key for Groq.

    Returns:
    str: Transcription text.
    """
    client = Groq(api_key=GROQ_API_KEY)

    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )

    return transcription.text

# Uncomment to transcribe audio
transcription_result = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
print("Transcription:", transcription_result)
