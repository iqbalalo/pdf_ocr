import requests

files = {"file": open("testdata.pdf", 'rb')}
headers = {
    'Accept': "application/pdf",
    'Content-Type': "multipart/form-data",
    'Cache-Control': "no-cache"
}

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

result = requests.post(url, files=files, headers=headers)
print(result.json())
