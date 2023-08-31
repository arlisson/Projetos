from encodings import search_function
import requests
from bs4 import *
import time
import re
from urllib.parse import urlsplit
import json
import speech_recognition as sr
import gtts
import pyttsx3

rec = sr.Recognizer()

with sr.Microphone(1) as mic:
    rec.adjust_for_ambient_noise(mic)
    print('O que deseja saber?')
    audio = rec.listen(mic)
    text = rec.recognize_google(audio, language="pt-BR")


print(text)

speaker = pyttsx3.init()
voices = speaker.getProperty('voices')

speaker.setProperty('voice', voices[0].id)  # definindo linguagm do sistema
rate = speaker.getProperty('rate')  # definindo propriedade de velocidade
speaker.setProperty('rate', rate-25)  # definindo velocidade


url = 'https://www.google.com/search?q={}'.format(text)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)

content = response.content

site = BeautifulSoup(content, 'html.parser')

links = []
for i in site.find_all('a'):    
    links.append(i.get('href'))


for i in links:
    if str(i).startswith('https') and str(i).count('google')!=1:
        print(i)
        try:
            url = i
            headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

            response = requests.get(url, headers=headers)

            content = response.content

            site = BeautifulSoup(content, 'html.parser')

            print(site.get_text())
            speaker.say(site.get_text())
            speaker.runAndWait()
            

        except RuntimeError :
          print('Ocorreu algum erro!')
          

