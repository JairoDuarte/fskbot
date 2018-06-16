import requests
import time
import cloudinary
import cloudinary.uploader
import cloudinary.api
from credentials import API_KEY, API_SECRET, CLOUD_NAME
import cloudconvert

api = cloudconvert.Api('qVjwVgld8qIDffvSHsMoO3tYCYtPzX8BS1P4LHRnm047RB5JOWiwVQQ28sQUb7Hq')

cloudinary.config(cloud_name=CLOUD_NAME, api_key=API_KEY, api_secret=API_SECRET)

"""
permet de convertir le fichier audio mp4 en prevenance de messenger en mp3
"""


def convert_download_audio(url_file, name):
    v_name = str(name).split('.')
    destination = v_name[0] + str((lambda: int(round(time.time() * 1000)))())
    print(v_name[-1])
    process = api.convert({
        "inputformat": v_name[-1],
        "outputformat": "wav",
        "input": "download",
        "filename": destination+'.'+v_name[-1],
        "file": url_file
    })
    print(destination)
    process.wait()
    process.download()
    return destination + '.wav'

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
    response = cloudinary.uploader.upload(file_path, resource_type="video")
    return str(response['url'])


if __name__ == '__main__':
    file = 'rec_9s.mp3'
    # download_file(YOUR_AUDIO_FILE, file)
    convert_to_audio(file)
