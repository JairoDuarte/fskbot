import subprocess as sp, os, traceback

# path to ffmpeg bin
FFMPEG_PATH = os.environ['FFMPEG_PATH'] if 'FFMPEG_PATH' in os.environ else '/usr/local/bin/ffmpeg'

import requests
from ffmpy import FFmpeg
import os
PATH = os.path.dirname(os.path.abspath(__file__))
#ffmpeg = PATH + "/ffmpeg/ffmpeg"

ff = FFmpeg(inputs={'audioclip-1526580982000-5376.mp4': None},outputs={'audioclip-1526580982000-5376.wav': None})
ff.cmd
ff.run()

def convert(file_path):
    try:
        command = [
            FFMPEG_PATH, '-i', file_path, '-y', '-loglevel', '16', '-threads', '8', '-c:v', 'mp4', '-f', 'wav', '-'
        ]
        # Get raw audio from stdout of ffmpeg shell command
        pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
        raw_audio = pipe.stdout.read()
        return raw_audio

    except Exception:
        print(Exception)


traceback.print_exc()