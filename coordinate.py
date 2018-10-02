class Coordinate:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        
    def toJSON(self):
        return{"Coordinate": {'lat': self.lat, 'lon': self.lon}}