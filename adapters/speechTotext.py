import json
import requests

YOUR_API_KEY = 'fc511417db424bce879829c573bae41b'
YOUR_AUDIO_FILE = 'http://res.cloudinary.com/angoticket/video/upload/v1524933963/rec_9s.mp3'
MODE = 'interactive'
LANG = 'Fr-Fr'
FORMAT = 'simple'

def handler(url):
    # 1. Get an Authorization Token
    token = get_token()
    # 2. Perform Speech Recognition
    results = get_text(token, url)
    # 3. Print Results
    print(results)

def get_token():
    # Return an Authorization Token by making a HTTP POST request to Cognitive Services with a valid API key.
    url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': YOUR_API_KEY
    }
    r = requests.post(url, headers=headers)
    token = r.content
    return(token)

def get_text(token, audio):
    # Request that the Bing Speech API convert the audio to text
    url = 'https://speech.platform.bing.com/speech/recognition/{0}/cognitiveservices/v1?language={1}&format={2}'.format(MODE, LANG, FORMAT)
    headers = {
        'Accept': 'application/json',
        'Ocp-Apim-Subscription-Key': YOUR_API_KEY,
        'Transfer-Encoding': 'chunked',
        'Content-type': 'audio/wav; codec=audio/pcm; samplerate=16000',
        'Authorization': 'Bearer {0}'.format(token)
    }
    r = requests.post(url, headers=headers, data=stream_audio_file(audio))
    results = json.loads(r.content)
    return results

def stream_audio_file(speech_file, chunk_size=1024):
    # Chunk audio file
    file_name = speech_file.split('/')[-1]
    print(file_name)
    file_name = file_name.split('?')[0]

    print(file_name)
    download_audio(speech_file,file_name)

    with open(file_name, 'rb') as f:
        while 1:
            data = f.read(1024)
            if not data:
                break
            yield data


def download_audio(url,file_name):
    r = requests.get(url)
    with open(file_name, 'wb') as f:
        try:
            for block in r.iter_content(1024):
                f.write(block)
                if not block:
                    return file_name;
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    handler()