import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_cors import CORS
from dao import DAO
import requests
import base64
import json


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'secret key'
CORS(app)
db = DAO()


@app.route('/')
def index():
    # load history
    history = db.get_history()

    return render_template("index.html", history=history)


@app.route('/submit_pdf', methods=["POST"])
def submit_pdf():
    request.files["pdf"].save(basedir + "/test.pdf")

    # call api to convert pdf to image
    result = convert_pdf_to_image(basedir + "/test.pdf")

    if "error_code" in result:
        flash(result)
        return redirect(url_for("index"))

    parent_id = result.get("parent_id", None)
    lid = result.get("lid", None)

    # convert image base64 to image
    img = result.get("image", None)
    if img:
        img = base64_to_image(img[0])

    if img is not None and os.path.exists(img):
        result = image_to_ocr(img)

    if "error" in result or not result:
        flash(result)
        return redirect(url_for("index"))

    # save to db
    res = db.create_history(lid=lid, parent_id=parent_id, result=result)

    if res:
        flash({"lid": lid, "parent_id": parent_id, "result": result})
    else:
        flash("OCR Data could not saved!")

    return redirect(url_for("index"))


def convert_pdf_to_image(pdf):
    file = {'file': open(pdf, 'rb')}
    url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

    result = requests.post(url, files=file)
    result = result.json()

    return result.get("data", None)


def base64_to_image(img_data):
    img_data = img_data.split(",")[1]
    img_data = bytes(img_data, 'utf-8')
    with open("test.jpeg", "wb") as fh:
        fh.write(base64.decodebytes(img_data))

    return "test.jpeg"


def image_to_ocr(image):
    file = {"file": open(basedir + "/" + image, 'rb')}
    url = "https://api-sandbox.fastaccounting.jp/v1.3/receipt"

    result = requests.post(url, files=file)
    result = result.json()
    result = json.dumps(result).encode("utf8")
    result = json.loads(result)

    text = ""
    for i in result.keys():
        text += "{}: {}\n".format(i, result[i])
    return text


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
