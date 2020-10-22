import requests
from jmespath import search

def create_user(payload, token, environment_url, org_id):
    # maybe should go to a different URL
    staff_url = f"{environment_url}/classes/organization/{org_id}/staff/"
    auth_header = {'Authorization': f"Bearer {token}"}
    response = requests.post(staff_url, json=payload, headers=auth_header)

    return response