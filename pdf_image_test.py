import requests
import os
import base64
import imghdr

def base64_to_image(img_data):
    # img_data = img_data.decode("utf-8")
    img_data = img_data.split(",")[1]
    img_data = bytes(img_data, 'utf-8')
    with open("test.jpeg", "wb") as fh:
        fh.write(base64.decodebytes(img_data))

    print(imghdr.what(basedir + "/test.jpeg"))
    return "test.jpeg"


basedir = os.path.abspath(os.path.dirname(__file__))

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

file = {'file': open(basedir + "/testdata.pdf", 'rb')}

result = requests.post(url, files=file)
result = result.json()
img_data = result.get("data", None)["image"][0]
print("image data type", type(img_data))
img_file = base64_to_image(img_data)

file = {"file": open(basedir + "/" + img_file, 'rb')}
# header = {'Content-Type': 'application/x-www-form-urlencoded'}
url = "https://api-sandbox.fastaccounting.jp/v1.3/receipt"

result = requests.post(url, files=file)
print(result.json())