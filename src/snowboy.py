import pyaudio
import snowboydecoder
import sys
import signal
#import RPi.GPIO as GPIO
import time
import os
import subprocess
import speech_recognition as sr
import urllib.request
from tts import say
import random

##### Настройки #####
#Название файлов модели. 
model1 = 'privet-alice.pmdl'
model2 = 'alice_privet.pmdl'

#Адрес до MajorDomo 
urlmjd = 'http://192.168.2.62'

home = os.path.abspath(os.path.dirname(__file__)) 


subprocess.Popen(["aplay", home+"/snd/Startup.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

interrupted = False

#Ссылки на голосовые модели

models = [home+'/resources/'+model1, home+'/resources/'+model2]

def signal_handler(signal, frame):
    global interrupted
    interrupted = True



def interrupt_callback():
    global interrupted
    return interrupted

def detected():
    try:
        #snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        subprocess.Popen(["aplay", home+"/snd/ding.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        index = pyaudio.PyAudio().get_device_count() - 1
        print (index)
        r = sr.Recognizer()
        with sr.Microphone(device_index=0) as source:
            r.adjust_for_ambient_noise(source) # Слушаем шум 1 секунду, потом распознаем, если раздажает задержка можно закомментировать.
            random_item = random.SystemRandom().choice(["Привет", "Слушаю", "На связи", "Да госпадин"])
            say (random_item)
            audio = r.listen(source, timeout = 10)
            subprocess.Popen(["aplay", home+"/snd/dong.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
            print("Processing !")
            #command=r.recognize_wit(audio, key="2S2VKVFO5X7353BN4X6YBX56L4S2IZT4")
            command=r.recognize_google(audio, language="ru-RU")
            print(command)
            subprocess.Popen(["aplay", home+"/snd/dong.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
            link=urlmjd+'/command.php?qry=' + urllib.parse.quote_plus(command)
            f=urllib.request.urlopen(link)
    except  sr.UnknownValueError:
        random_item = random.SystemRandom().choice(["Вы что то сказали ?", "Я ничего не услышала", "Что Вы спросили?", "Не поняла"])
        say (random_item)
        detected

    except sr.RequestError as e:
        print("Произошла ошибка  {0}".format(e))
        say ("Произошла ошибка  {0}".format(e))

    except sr.WaitTimeoutError:
        print ("Я ничего не услышала")
        say ("Я ничего не услышала")

#capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models) #уровень распознования, чем больше значение, тем больше ложных срабатываней
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [detected, detected]
print('Слушаю... Нажмите Ctrl+C для выхода')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)

detector.terminate()
