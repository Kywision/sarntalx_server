#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for, send_from_directory, json
from werkzeug.utils import secure_filename
import os
from coordinate import Coordinate
from classifier import Classifier
from PIL import Image
import base64   


UPLOAD_FOLDER = '/images/'
ALLOWED_EXTENSIONS = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/receive", methods=['POST'])
def receiveDronePictures():
    if request.method == 'POST':

        

        file = request.get_data()
        print('file received')
        
        with open('tmp.jpg', 'wb') as fh:
            fh.write(base64.decodebytes(file))

        img = Image.open('tmp.jpg')
        detector = Classifier()
        results = detector.detect(img)

        print(results)
        json = results.toJSON
        return json




if __name__ == "__main__":
    
    app.run(host='0.0.0.0')




