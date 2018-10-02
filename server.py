#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for, send_from_directory, json
from werkzeug.utils import secure_filename
import os
from coordinate import Coordinate
from random import randint

UPLOAD_FOLDER = '/images/'
ALLOWED_EXTENSIONS = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/receive", methods=['POST'])
def receive():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join[app.config['UPLOAD_FOLDER'], 'filename'])
    co = Coordinate('20', '40')
    jsonStr = json.dumps(co.toJSON())



if __name__ == "__main__":
    
    app.run(host='0.0.0.0', debug=True)




