from encodings import search_function
from fnmatch import translate
import requests
from bs4 import *
import time
import re
from urllib.parse import urlsplit
import json
import speech_recognition as sr
import gtts
import pyttsx3
from googletrans import Translator

translator = Translator()


def escutar():
    rec = sr.Recognizer()
    with sr.Microphone(1) as mic:
        rec.adjust_for_ambient_noise(mic)
        print('Fale')
        audio = rec.listen(mic)
        text = rec.recognize_google(audio_data=audio, language='pt-BR')

    text = str(text).upper()
    print(text)
    if(text == 'BARRA SAIR'):
        exit()
    return text


while True:

    speaker = pyttsx3.init()
    voices = speaker.getProperty('voices')
    speaker.setProperty('voice', voices[1].id)  # definindo linguagm do sistema
    rate = speaker.getProperty('rate')  # definindo propriedade de velocidade
    speaker.setProperty('rate', rate-25)  # definindo velocidade

    res = translator.translate(escutar(), dest='en').get_text()

    print(res)
    speaker.say(res)
    speaker.runAndWait()
    time.sleep(1)
