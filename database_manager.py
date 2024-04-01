import requests


class DatabaseManager:
    def __init__(self, url):
        self.url = url

    def get_character_info_by_name(self, name):
        params = {"name": name}
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
