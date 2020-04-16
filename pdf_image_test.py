import requests
import os

basedir = os.path.abspath(os.path.dirname(__file__))

pdf = open(basedir + "/testdata.pdf", 'rb')
pdf_binary = pdf.read()
files = {"file": pdf_binary}
headers = {
    'Content-Type': "multipart/form-data"
}

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

result = requests.post(url, files=files, headers=headers)
print(result.json())
