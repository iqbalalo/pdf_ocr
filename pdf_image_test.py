import requests
import os
import base64

basedir = os.path.abspath(os.path.dirname(__file__))


with open(basedir + "/testdata.pdf", "rb") as pdf_file:
    encoded_string = base64.b64encode(pdf_file.read())

files = {"file": encoded_string}
headers = {
    'Content-Type': "multipart/form-data"
}

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

result = requests.post(url, files=files, headers=headers)
print(result.json())
