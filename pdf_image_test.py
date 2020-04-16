import requests
import os

basedir = os.path.abspath(os.path.dirname(__file__))

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

data = open(basedir + "/testdata.pdf", 'rb').read()
headers = {
    "Content-Type":"application/binary"
}
result = requests.post(url, files=dict(file=data), headers=headers)
print(result.json())
