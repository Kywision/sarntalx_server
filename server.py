#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

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


if __name__ == "__main__":
    
    app.run(host='0.0.0.0')




