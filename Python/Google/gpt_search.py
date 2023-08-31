import requests
from bs4 import *
import time
import re
from urllib.parse import urlsplit
import json

apikey = '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'
model_id = 'gpt-3.5-turbo'
headers = {"Authorization": f"Bearer {apikey}",
           "Content-Type": "application/json"}

url = 'https://api.openai.com/v1/chat/completions'

body_message = {
    "model": "gpt-3.5-turbo",
    "messages": [{
        "role": "user",
        "content": "Quem é Duque de Caxias?"
    }]}

body_message = json.dumps(body_message)


response = requests.post(url, headers=headers, data=body_message)

print(response)
print(response.text)
