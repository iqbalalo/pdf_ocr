import os
import pycurl
from io import BytesIO

buffer = BytesIO()

basedir = os.path.abspath(os.path.dirname(__file__))
url = "https://api-sandbox.fastaccounting.jp/v1.3/convert_to_jpg"

c = pycurl.Curl()
c.setopt(c.URL, 'https://httpbin.org/post')
c.setopt(c.HTTPPOST, [("file", (c.FORM_FILE, basedir + "/testdata.pdf"))])
c.perform()
c.close()
body = buffer.getvalue()
print(body)