import json
import requests
from speech.utils import convert_to_audio, download_file
from credentials import MS_YOUR_API_KEY
import os


YOUR_AUDIO_FILE = 'http://res.cloudinary.com/angoticket/video/upload/v1524933963/rec_9s.mp3'
MODE = 'conversation'
LANG = 'Fr-Fr'
FORMAT = 'simple'


def speech_to_text(url):
    # 1. Get an Authorization Token
    token = get_token()
    # 2. Perform Speech Recognition
    results = get_text(token, url)
    # 3. Print Results
    print(results)
    return results.get('DisplayText')


# Retourne un token d'authorization pour l'execution d'une requete POST sur azure  Cognitive Services.

def get_token():
    url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': MS_YOUR_API_KEY
    }
    r = requests.post(url, headers=headers)
    token = r.content
    return (token)


# Requete qui envois le fichier audio en stream vers  Bing Speech API pour convertir l'audio en text et retourne un json

def get_text(token, audio):
    url = 'https://speech.platform.bing.com/speech/recognition/{0}/cognitiveservices/v1?language={1}&format={2}'.format(
        MODE, LANG, FORMAT)
    headers = {
        'Accept': 'application/json',
        'Ocp-Apim-Subscription-Key': MS_YOUR_API_KEY,
        'Transfer-Encoding': 'chunked',
        'Content-type': 'audio/wav; codec=audio/pcm; samplerate=16000',
        'Authorization': 'Bearer {0}'.format(token)
    }
    try:
        r = requests.post(url, headers=headers, data=stream_audio_file(audio))
        results = json.loads(r.content)
    except KeyboardInterrupt:
        pass

    return results


# Execute le fichier audio en streaming

def stream_audio_file(speech_file, chunk_size=1024):
    file_name = speech_file.split('/')[-1]
    file_name = file_name.split('?')[0]
    download_file(speech_file, file_name)
    destination = convert_to_audio(file_name)
    #file_name = 'audioclip-1526667515000-8576.wav'
    #destination = 'audioclip-1526675322000-9088.wav'
    print(destination)
    with open(destination, 'rb') as f:
        while 1:
            data = f.read(1024)
            if not data:
                break
            yield data
