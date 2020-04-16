import requests
import os
import base64
import imghdr

def base64_to_image(img_str):
    img_str += "=" * ((4 - len(img_str) % 4) % 4)
    img_data = base64.urlsafe_b64decode(img_str)
    print(img_data)
    with open("test.jpeg", "wb") as fh:
        fh.write(base64.decodebytes(img_data))
    return "test.jpeg"

basedir = os.path.abspath(os.path.dirname(__file__))

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

file = {'file': open(basedir + "/testdata.pdf", 'rb')}

result = requests.post(url, files=file)
result = result.json()
img_file = base64_to_image(result.get("data", None)["image"][0])

print("image type", imghdr.what(basedir + "/" + img_file))

file = {"file": open(basedir + "/" + img_file, 'rb')}
# header = {'Content-Type': 'application/x-www-form-urlencoded'}
url = "https://api-sandbox.fastaccounting.jp/v1.3/receipt"

result = requests.post(url, files=file)
print(result.json())