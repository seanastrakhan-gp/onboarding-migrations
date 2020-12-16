import requests
from jmespath import search
from application.settings import cache, USERNAME, PASSWORD, ENV_HOST
from application.services.authenticate import authenticate

TOKEN_CACHE_KEY = 'auth_token'


def set_new_auth():
    token = authenticate(USERNAME, PASSWORD)
    cache[TOKEN_CACHE_KEY] = token
    return token


def get_role():
    # where we have to take current user role
    auth_url = f"{ENV_HOST}/account/profile/"
    response = authorized_request('get', auth_url)
    token = search('type', response.json())
    return token


def api_call(method, *args, **kwargs):
    headers = kwargs.pop('headers', dict()) or dict()
    token = cache.get(TOKEN_CACHE_KEY)
    headers['Authorization'] = f"Bearer {token}"
    return getattr(requests, method.lower())(*args, headers=headers, **kwargs)


def authorized_request(method, *args, **kwargs):
    """Make an attempt with new credentials in case of 401"""
    response = api_call(method, *args, **kwargs)
    if response.status_code == 401:
        set_new_auth()
        response = api_call(method, *args, **kwargs)
    return response
