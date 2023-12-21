
import requests
from bs4 import *

url = 'http://localhost:8080/deletepersonid'

response = requests.delete(url, json = {"id":2})


print(response)
