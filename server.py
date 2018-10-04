#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from coordinate import Coordinate
from classifier import Classifier

from PIL import Image
import base64
from io import BytesIO
import json


UPLOAD_FOLDER = '/images/'
ALLOWED_EXTENSIONS = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DETECTOR = Classifier()


@app.route("/detect", methods=['POST'])
def receiveDronePictures():
    file = request.get_data()
    print('file received')
    img = Image.open(BytesIO(base64.b64decode(file)))
    results = DETECTOR.detect(img, None)
    json_data= json.dumps(results)
    print(json_data)
    return json_data

if __name__ == "__main__":
    app.run(host='localhost')
