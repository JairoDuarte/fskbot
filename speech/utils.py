import requests
from ffmpy import FFmpeg
import os
import time
import cloudinary
import cloudinary.uploader
import cloudinary.api
from credentials import API_KEY, API_SECRET, CLOUD_NAME

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

"""
permet de convertir le fichier audio mp4 en prevenance de messenger en mp3
"""

def convert_to_audio(file_path):
    source = file_path
    destination = str(file_path).split('.')[0] + str((lambda: int(round(time.time() * 1000)))()) + '.wav'
    try:
        ff = FFmpeg(inputs={source: None},
                    outputs={destination: None})
        ff.run()
    except Exception:
        print(Exception)
    return destination


"""
permet de telecharger un fichier
"""


def download_file(url, file_name):
    response = requests.get(url, allow_redirects=True)

    try:
        open(file_name, 'wb').write(response.content)
    except KeyboardInterrupt:
        pass


def upload_audio(file_path):
    response = cloudinary.uploader.upload(file_path, resource_type = "raw") #cloudinary.uploader.upload(file_path)
    return str(response['url'])


if __name__ == '__main__':
    file = 'rec_9s.mp3'
    # download_file(YOUR_AUDIO_FILE, file)
    convert_to_audio(file)
