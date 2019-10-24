from InstagramRetriever import InstagramRetriever
from TwitterRetriever import TwitterRetriever
from CredentialsReader import CredentialsReader
from SatelliteRetriever import SatelliteRetriever
from ResultSaver import ResultSaver
from Locator import Locator

address = "Brusselsesteenweg 202, 9090 Melle"

# Get credentials
credentials = CredentialsReader().load()

# Get location from address
location = Locator().getLatLong(address)

# Get the latest images from that location from instagram
instagram = InstagramRetriever(credentials['instagram']['login'], credentials['instagram']['password'])
instagram.login()
images = instagram.getImages(location['lat'], location['long'])
print('Images: ' + str(images.count))

# Get the latest tweets from that location
twitter = TwitterRetriever(credentials['twitter']['key'], credentials['twitter']['secret'])
twitter.login()
tweets = twitter.getTweets(location['lat'], location['long'])
print('Tweets: ' + str(tweets.count))

satellite = SatelliteRetriever(credentials['copernicus']['login'], credentials['copernicus']['password'])
satellite.login()
satelliteImages = satellite.getAvailableImages(location['lat'], location['long'])
# TODO: Get strava flybys 
# TODO: find cam feeds in the neighbourhood (https://medium.com/@woj_ciech/%EA%93%98amerka-build-interactive-map-of-cameras-from-shodan-a0267849ec0a) 
# TODO: find other services with location & time information

ResultSaver().SaveTemplate(address, tweets, images, satelliteImages)