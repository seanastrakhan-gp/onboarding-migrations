import requests
from jmespath import search


def authenticate(username, password):
    auth_url = f"{ENV_HOST}/account/login/"
    response = requests.post(auth_url, json={'username': username, 'password': password})

    if response.status_code == 200:
        token = search('access_token', response.json())
        return token


def get_role(token):
    # where we have to take current user role
    pass