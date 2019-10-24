from sentinelsat.sentinel import SentinelAPI

class SatelliteRetriever:
    
    def __init__(self, login, password):
        self.username = login
        self.password = password

    def login(self):
        self.api = SentinelAPI(self.username, self.password, 'https://scihub.copernicus.eu/dhus')

    def getAvailableImages(self, lat, long):
        products = self.api.query_raw('beginposition:[2019-10-01T00:00:00.000Z TO NOW] footprint:"intersects(' + str(lat) + ',' + str(long) + ')" L0')
        images = []
        for productId in products:
            product = products[productId]
            time = product['beginposition'].strftime('%s')
            images.append({'url': product['link'], 'name': product['title'], 'time': int(time)})
        return images