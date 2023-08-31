from encodings import search_function
import requests
from bs4 import *
import time
import re
from urllib.parse import urlsplit
import json


apigoogle = '535839478340-fa6qfec20kfnctghhc8h8f3pp1ps4lp4.apps.googleusercontent.com'

url = 'https://www.ebiografia.com/duque_caxias/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)

content = response.content

site = BeautifulSoup(content, 'html.parser')

print(site.get_text())