import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import date


response = requests.get('https://alternative.me/crypto/fear-and-greed-index/')

content = response.content

site = BeautifulSoup(content, 'html.parser')

medo_mercado = site.findAll('div', attrs={'class': 'fng-circle'})
medo_texto = site.findAll('div', attrs={'class': 'status'})
medo_desc = site.findAll('div', attrs={'class': 'gray'})
medo = int(medo_mercado[0].text)
msgm = []

data = date.today()

for i in range(len(medo_mercado)):
    msgm.append('{}: {} pontos {}'.format(
        medo_desc[i].text, medo_mercado[i].text, medo_texto[i].text))


email_adress = 'robomensageiro4321@gmail.com'
destinatario = 'arlisson234529@gmail.com'
senha = 'ciounqbgujbtumly'
mensagem = '{}\n{}\n{}\n{}\n\nData:{}/{}/{}'.format(
    msgm[0], msgm[1], msgm[2], msgm[3], data.day, data.month, data.year)

print(mensagem)


if(medo <= 20):
    msg = EmailMessage()
    msg['Subject'] = 'Atualização Sobre o Mercado de Cripto'
    msg['From'] = email_adress
    msg['To'] = destinatario
    msg.set_content(mensagem)
else:
    msg = EmailMessage()
    msg['Subject'] = 'Atualização Sobre o Mercado de Cripto'
    msg['From'] = email_adress
    msg['To'] = destinatario
    msg.set_content(mensagem)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_adress, senha)
    smtp.send_message(msg)
