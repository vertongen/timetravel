import json
import codecs
import datetime
import os.path
try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)

class InstagramRetriever:
    def __init__(self, login, password):
        self.username = login
        self.password = password
    
    def to_json(self, python_object):
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': codecs.encode(python_object, 'base64').decode()}
        raise TypeError(repr(python_object) + ' is not JSON serializable')


    def from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object


    def onloginCallback(self, api, new_settings_file):
        cache_settings = api.settings
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default=self.to_json)
            print('SAVED: {0!s}'.format(new_settings_file))

    def login(self):
        settingsFile = 'settings.json'
        try:
            if not os.path.isfile(settingsFile):
                self.api = Client(self.username, self.password, 
                on_login=lambda x: self.onloginCallback(x, settingsFile))
            else:
                with open('settings.json') as file_data:
                    self.cached_settings = json.load(file_data, object_hook=self.from_json)
                self.api = Client(self.username, self.password, settings=self.cached_settings)
        except  (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            # Login expired
            # Do relogin but use default ua, keys and such
            self.api = Client(self.username, self.password,
                on_login=lambda x: self.onloginCallback(x, settingsFile))
        except ClientLoginError as e:
            print('ClientLoginError {0!s}'.format(e))
            exit(9)
        except ClientError as e:
            print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
            exit(9)
        except Exception as e:
            print('Unexpected Exception: {0!s}'.format(e))
            exit(99)

    def getImages(self,lat,long):
        locations = self.from_json(self.api.location_search(lat,long))

        external_id = locations['venues'][0]['external_id']
        uuid = self.api.generate_uuid()
        stories = self.api.location_section(external_id, uuid, 'recent')

        with open('stories.json', 'w+') as file_data:
            file_data.write(json.dumps(stories))
        
        images = []
        for section in stories['sections']:
            
            for media in section['layout_content']['medias']:
                url = "https://www.instagram.com/p/" + media['media']['code'] + "/"
                if 'image_versions2' in media['media']:
                    imageUrl = media['media']['image_versions2']['candidates'][0]['url']
                    images.append({'imageUrl': imageUrl, 'time': media['media']['taken_at'], 'url': url})
                elif 'carousel_media' in media['media']:
                    for image in media['media']['carousel_media']:
                        if 'image_versions2' in image:
                            imageUrl = image['image_versions2']['candidates'][0]['url']
                            images.append({'imageUrl': imageUrl, 'time': media['media']['taken_at'], 'url': url})
        return images