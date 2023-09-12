from encodings import search_function
import requests
from bs4 import *
import time
import re
from urllib.parse import urlsplit
import json




url = 'https://www.ebiografia.com/duque_caxias/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)

content = response.content

site = BeautifulSoup(content, 'html.parser')

print(site.get_text())
