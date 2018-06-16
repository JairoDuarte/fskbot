import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from speech.utils import download_file, convert_download_audio

YOUR_AUDIO_FILE = 'http://res.cloudinary.com/angoticket/video/upload/v1524933963/rec_9s.mp3'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "fskMaster-95193100d409.json"


def get_text(url):
    file_name = url.split('/')[-1]
    file_name = file_name.split('?')[0]
    print(url)
    destination = convert_download_audio(url, file_name)
    #destination = convert_to_audio(file_name)
    text = speech_to_text(destination)
    os.remove(destination)
    return text


def speech_to_text(file_name):
    # Instantiates a client
    client = speech.SpeechClient()
    # Loads the audio into memory

    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='fr-FR')

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    text = ''
    for result in response.results:
        text = text + ' ' + result.alternatives[0].transcript
    return text
