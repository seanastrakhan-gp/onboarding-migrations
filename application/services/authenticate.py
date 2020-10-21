import requests
from jmespath import search

def authenticate(username, password, environment_url):
    auth_url = f"{environment_url}/account/login/"
    response = requests.post(auth_url, json={'username': username, 'password': password})

    if response.status_code == 200:
        token = search('refresh_token', response.json())
        return token
        