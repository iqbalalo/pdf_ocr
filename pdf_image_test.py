import requests
import os
import base64
import re


def decode_base64(data, altchars=b'+/'):
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)


def base64_to_image(img_str):
    img_data = decode_base64(img_str)
    filename = 'test.jpg'
    with open(filename, 'wb') as f:
        f.write(img_data)
    return filename


basedir = os.path.abspath(os.path.dirname(__file__))

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

file = {'file': open(basedir + "/testdata.pdf", 'rb')}

result = requests.post(url, files=file)
result = result.json()
print(result.get("data", None)["image"][0])
base64_to_image(result.get("data", None)["image"][0])
