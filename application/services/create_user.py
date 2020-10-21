import requests
from jmespath import search

def create_user(payload, token, environment_url):
    # maybe should go to a different URL
    staff_url = f"{environment_url}/classes/organization/staff/"
    auth_header = {'Authorization': f"Bearer {token}"}
    response = requests.post(staff_url, json=payload, headers=auth_header)

    if response.status_code == 200:
        token = search('access_token', response.json())
        return token
        