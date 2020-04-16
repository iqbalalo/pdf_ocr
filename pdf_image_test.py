import requests
import os

basedir = os.path.abspath(os.path.dirname(__file__))

files = {"file": open(basedir + "/testdata.pdf", 'rb').read()}
headers = {
    'Content-Type': "multipart/form-data"
}

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

result = requests.post(url, files=files, headers=headers)
print(result.json())
