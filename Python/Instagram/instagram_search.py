import requests
from bs4 import *
from urllib.parse import urlsplit
import json

url = 'https://www.facebook.com/arlisson.alvesdasilvasilveira'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)

content = response.content

site = BeautifulSoup(content, 'html.parser')

#a = site.find_all('')
print(site.get_text())