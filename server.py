#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/images/'
ALLOWED_EXTENSIONS = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/calc_pattern", methods=['POST'])
def calc_pattern():
    """
    Calculates a search pattern for a given GPS coordinate and search pattern.

    Example payload:
    {
        "lat": 46.746205,
        "lon": 11.358717,
        "pattern": "sweep"
    }
    """
    payload = request.get_json(force=True)
    lat, lon = float(payload['lat']), float(payload['lon'])
    start_point = Point(lat, lon)
    pattern = pointcloud.generate_search_pattern(payload['pattern'], start_point, SAMPLING_DIST)
    enriched_pattern = pointcloud.add_elevation_data(pattern)

    response = '['
    for point in enriched_pattern:
        response += (str(point) + ",")
    return response[:-1] + ']'


@app.route("/receive/", methods=['POST'])
def receive():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join[app.config['UPLOAD_FOLDER'], filename])
            return redirect(url_for('uploaded_file'), filename=filename)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    ''' 

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    
    app.run(host='0.0.0.0', debug=True)




