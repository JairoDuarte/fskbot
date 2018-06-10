# def synthesize_text(text):
"""Synthesizes speech from the input string of text."""

from google.cloud import texttospeech
import os, time

from speech.utils import upload_audio

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jairoduarte/fskMaster-95193100d409.json"
client = texttospeech.TextToSpeechClient()

text = 'Passionné de BD comme les aventures d\'Astérix, de romans, polars ou de Sciences-Humaines ? ' \
       'Retrouvez à la Fnac toutes les nouveautés de vos auteurs préférés. Suivez les conseils de nos experts en littérature, ' \
       'Science-fiction ou roman adolescent et découvrez le blog du Cercle Littéraire, un espace où des adhérents - grands lecteurs' \
       ' partagent leurs coups de cœur. Ne manquez aucune promotion pour vous offrir de beaux livres ! Téléchargez aussi des millions ' \
       'd’ebooks à lire sur les liseuses Kobo ou sur l’application gratuite Kobo by Fnac.'



def get_url(message):
    file_name = text_speech(message)
    print(file_name)
    url = upload_audio(file_name)
    return url


def text_speech(message):
    input_text = texttospeech.types.SynthesisInput(text=message)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='fr-FR',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)
    destination = '../output' + str((lambda: int(round(time.time() * 1000)))()) + '.mp3'

    # The response's audio_content is binary.
    with open(destination, 'wb') as out:
        out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
    return destination


print(get_url(text))