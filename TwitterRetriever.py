from twython import Twython
import json
import time

class TwitterRetriever:
    
    def __init__(self, login, password):
        self.username = login
        self.password = password

    def login(self):
        self.api = Twython(self.username, self.password)
        print('logged into twitter')

    def getTweets(self, lat, long):

        # TODO: get geocoded coordinates from pypieter_tools.py
        query = {
            'geocode': str(lat) + ',' + str(long) + ',1mi',
            'q': ' ',
            'result_type': 'recent',
            'count': 50,
        }
        print(query)

        # Search tweets
        tweets = []
        for status in self.api.search(**query)['statuses']:
            ts = time.mktime(time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

            tweets.append({
                'user': status['user']['screen_name'],
                'time': ts,
                'text': status['text'] + ' (' + status['created_at'] + ')',
                'url': f'https://twitter.com/i/web/status/{status["id_str"]}',
                'favorite_count': status['favorite_count']
            })

        return tweets