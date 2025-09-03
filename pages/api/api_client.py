import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def get(self, endpoint, headers=None):
        return requests.get(self.base_url + endpoint, headers=headers)

    def post(self, endpoint, json=None, headers=None):
        return requests.post(self.base_url + endpoint, json=json, headers=headers)
