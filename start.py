from InstagramRetriever import InstagramRetriever
from TwitterRetriever import TwitterRetriever
from CredentialsReader import CredentialsReader
from ResultSaver import ResultSaver
from Locator import Locator

address = "Wortegemstraat 119, oudenaarde"

# Get credentials
credentials = CredentialsReader().load()

# Get location from address
location = Locator().getLatLong(address)

# Get the latest images from that location from instagram
instagram = InstagramRetriever(credentials['instagram']['login'], credentials['instagram']['password'])
instagram.login()
images = instagram.getImages(location['lat'], location['long'])

# Get the latest tweets from that location
twitter = TwitterRetriever(credentials['twitter']['key'], credentials['twitter']['secret'])
twitter.login()
tweets = twitter.getTweets(location['lat'], location['long'])

ResultSaver().SaveTemplate(address,  tweets, images)