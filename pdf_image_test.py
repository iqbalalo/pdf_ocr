import requests
import os

basedir = os.path.abspath(os.path.dirname(__file__))

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

result = requests.post(url, files=dict(file=(basedir + "/testdata.pdf")))
print(result.json())
