import snowboydecoder
import sys
import signal
#import RPi.GPIO as GPIO
import time
import os
import subprocess
import speech_recognition as sr
import urllib.request
import simpleaudio as sa
from tts import say

subprocess.Popen(["aplay", "~/mdmOrangePiZeroTerminal/src/snd/Startup.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

interrupted = False

#Ссылки на голосовые модели 
models = ['~/mdmOrangePiZeroTerminal/src/resources/privet.pmdl']

def signal_handler(signal, frame):
    global interrupted
    interrupted = True



def interrupt_callback():
    global interrupted
    return interrupted

def detected():
   try:
       snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
       say ("Слушаю !")
       r = sr.Recognizer()
       with sr.Microphone(2) as source: # Микрофон включается на 2 устройстве 
           r.adjust_for_ambient_noise(source)  # Слушаем шум 1 секунду, потом распознаем, если раздажает задержка можно закомментировать. 
           audio = r.listen(source, timeout = 10)
           snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
           print("Processing !")
#          print(r.recognize_wit(audio, key="ключ WIT"))
#          command=r.recognize_wit(audio, key="ключ WIT")
           command=r.recognize_google(audio,language="ru-RU")
           print(command)
           snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
           link='http://192.168.1.10/command.php?qry=' + urllib.parse.quote_plus(command)
           f=urllib.request.urlopen(link)
   except  sr.UnknownValueError:
           say("Я не понимаю, что ты сказал.")
           detected

   except sr.RequestError as e:
           print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

   except sr.WaitTimeoutError:
           print ("Я ничего не услышала")
           say ("Я ничего не услышала")

#capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.3]*len(models) #уровень распознования, чем больше значение, тем больше ложных срабатываней 
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [detected]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
