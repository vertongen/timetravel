from geopy.geocoders import Nominatim

class Locator:
    def getLatLong(self, address):
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
        location = geolocator.geocode(address)
        return {'lat': location.latitude, 'long': location.longitude}
