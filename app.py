import os
from flask import Flask, render_template, redirect, url_for, request
from flask_cors import CORS
from dao import DAO
import requests
import base64


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_relative_config=True)
CORS(app)

db = DAO()
ocr_result = ""


@app.route('/')
def index():
    global ocr_result

    # load history
    history = db.get_history()

    return render_template("index.html", ocr_result=ocr_result, history=history)


@app.route('/submit_pdf', methods=["POST"])
def submit_pdf():
    global ocr_result
    request.files["pdf"].save(basedir + "/test.pdf")

    result = convert_pdf_to_image(basedir + "/test.pdf")

    if result is None:
        ocr_result = "Invalid PDF!"
        return redirect(url_for("index"))

    parent_id = result["parent_id"]
    lid = result["lid"]
    image = base64_to_image(result["image"][0])

    if os.path.exists(image):
        result = image_to_ocr(image)

    if not result:
        ocr_result = "Invalid PDF to OCR Data!"
        return redirect(url_for("index"))

    # save to db
    res = db.create_history(lid=lid, parent_id=parent_id, result=result)

    # load to ocr_result
    if res:
        ocr_result = {"lid": lid, "parent_id": parent_id, "result": result}
    else:
        ocr_result = "OCR Data could not saved!"

    return redirect(url_for("index"))


def convert_pdf_to_image(pdf):
    file = {'file': open(basedir + "/" + pdf, 'rb')}
    url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

    result = requests.post(url, files=file)
    result = result.json()

    return result.get("data", None)


def base64_to_image(img_str):
    img_str += "=" * ((4 - len(img_str) % 4) % 4)
    img_data = base64.b64decode(img_str)
    filename = 'test.jpg'
    with open(filename, 'wb') as f:
        f.write(img_data)
    return filename


def image_to_ocr(image):
    files = {"file": open(image, 'rb')}
    headers = {
        'Accept': "application/pdf",
        'Content-Type': "multipart/form-data",
        'Cache-Control': "no-cache"
    }
    url = "https://api-sandbox.fastaccounting.jp/v1.3/receipt"

    result = requests.post(url, files=files, headers=headers)
    print(result.json())

    if result and result["result"] == "SUCCESS":
        return result["data"]

    return None


if __name__ == "__main__":
    os.environ["FLASK_ENV"] = "development"
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
