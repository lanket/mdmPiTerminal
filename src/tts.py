from gtts import gTTS
from googletrans import Translator
from yandex_speech import TTS
import requests
import os
import os.path


##Speech and translator declarations
ttsfilename="/tmp/say.mp3"
translator = Translator()
language='ru'


#Text to speech converter with translation
def say(words):
    words= translator.translate(words, dest=language)
    words=words.text
    words=words.replace("Text, ",'',1)
    words=words.strip()
    print(words)
    #tts = gTTS(text=words, lang=language)
    tts = TTS("alyss", "mp3", "3a5d503c-d9a8-489d-a100-954294c36cf8",lang="ru-RU",emotion="good")
    tts.generate(words)
    tts.save(ttsfilename)
    os.system("mpg123 "+ttsfilename)
    os.remove(ttsfilename)

