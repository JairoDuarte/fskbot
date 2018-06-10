from gtts import gTTS
import os
text = 'Passionné de BD comme les aventures d\'Astérix, de romans, polars ou de Sciences-Humaines ? ' \
       'Retrouvez à la Fnac toutes les nouveautés de vos auteurs préférés. Suivez les conseils de nos experts en littérature, ' \
       'Science-fiction ou roman adolescent et découvrez le blog du Cercle Littéraire, un espace où des adhérents - grands lecteurs' \
       ' partagent leurs coups de cœur. Ne manquez aucune promotion pour vous offrir de beaux livres ! Téléchargez aussi des millions ' \
       'd’ebooks à lire sur les liseuses Kobo ou sur l’application gratuite Kobo by Fnac.'

tts = gTTS(text=text, lang='fr-fr')
filename = 'temp4.mp3'
tts.save(filename)
