import requests
import os
from pprint import pprint

basedir = os.path.abspath(os.path.dirname(__file__))

url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

result = requests.post(url, files=dict(file=(basedir + "/testdata.pdf")))
pprint(result.json()['headers'])
