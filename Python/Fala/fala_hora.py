import speech_recognition as sr
import requests
from bs4 import *
import gtts
import pyttsx3


def pegar_hora():

    url = 'https://www.horariodebrasilia.org/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)

    content = response.content

    site = BeautifulSoup(content, 'html.parser')

    hora = site.find('p', attrs={'id': 'relogio'})
    dia = site.find('h3', attrs={'id': 'dia-topo'})

    texto = 'A hora atual de Brasília é: {}'.format(hora.get_text())
    print(dia.get_text()+'\n{}'.format(texto))

    return dia.get_text()+'\n{}'.format(texto)


rec = sr.Recognizer()

with sr.Microphone(1) as mic:
    rec.adjust_for_ambient_noise(mic)
    print('Fale imediatamente')
    audio = rec.listen(mic)
    text = rec.recognize_google(audio, language="pt-BR")

text = text.upper()
print(text)


if(text == 'QUE HORAS SÃO'):

    speaker = pyttsx3.init()
    voices = speaker.getProperty('voices')

    speaker.setProperty('voice', voices[0].id)  # definindo linguagm do sistema
    rate = speaker.getProperty('rate')  # definindo propriedade de velocidade
    speaker.setProperty('rate', rate-25)  # definindo velocidade

    speaker.say(pegar_hora())  # dizer
    speaker.runAndWait()  # executar e falar


'''for voice in voices:
    print(voice,voice.id)'''
# print(sr.Microphone().list_microphone_names())
