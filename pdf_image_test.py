import requests
import os
import base64


def base64_to_image(img_str):
    img_data = base64.b64decode(img_str)
    filename = 'test.jpg'
    with open(filename, 'wb') as f:
        f.write(img_data)
    return filename

basedir = os.path.abspath(os.path.dirname(__file__))

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

file = {'file': open(basedir + "/testdata.pdf", 'rb')}

result = requests.post(url, files=file)
result = result.json()
base64_to_image(result.get("data", None)["image"][0])
