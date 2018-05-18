import requests
from ffmpy import FFmpeg

YOUR_AUDIO_FILE = 'http://res.cloudinary.com/angoticket/video/upload/v1524933963/rec_9s.mp3'

"""
permet de convertir le fichier audio mp4 en prevenance de messenger en mp3
"""


def convert_to_audio(file_path):
    source = file_path
    destination = str(file_path).split('.')[0] + '.wav'
    try:
        ff = FFmpeg(inputs={source: None},
                    outputs={destination: None})
        ff.run()

    except Exception:
        print(Exception)


def download_audio(url, file_name):
    response = requests.get(url, allow_redirects=True)

    try:
        open(file_name, 'wb').write(response.content)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    file = 'rec_9s.mp3'
    download_audio(YOUR_AUDIO_FILE, file)
    convert_to_audio(file)
