import requests
from requests.structures import CaseInsensitiveDict

url1 = "http://127.0.0.1:5000/api/v1/switch"
url2 = "http://127.0.0.1:5000/api/v1/ner"
url3 = "http://127.0.0.1:5000/api/v1/displacy"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = '{ "text": "Warszawa" }'

resp1 = requests.post(url1, headers=headers, data=data)
resp2 = requests.post(url2, headers=headers, data=data)
resp3 = requests.post(url3, headers=headers, data=data)


print(resp3.status_code)
print(resp3.text)
print(resp3.content)