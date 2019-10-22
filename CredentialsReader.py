import json

class CredentialsReader:
    def load(self): 
        with open("credentials.json", "r") as file:
            credentials = json.load(file)
            return credentials
        return {}