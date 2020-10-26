import requests
from jmespath import search
from application.utils.csv import generate_csv
from application.settings import ENV_HOST

STUDENT_BULK_REGISTRATION_PARAMS = (
    'id',
    'first_name',
    'last_name',
    'birthdate',
    'gender',
    'address',
    'address_2',
    'city',
    'zipcode',
    'country',
)

STAFF_BULK_PARAMS = (
    'first_name',
    'last_name',
    'username',
    'password',
    'email',
    'mobile',
    'staff_role_name',
    'staff_role'
)

def create_staff(payload, token, org_id):
    # maybe should go to a different URL
    url = f"{ENV_HOST}/classes/organization/{org_id}/staff/"
    auth_header = {'Authorization': f"Bearer {token}"}
    response = requests.post(url, json=payload, headers=auth_header)
    return response

def create_student(payload, token, org_id):
    url = f"{ENV_HOST}/classes/organization/{org_id}/student_user/"
    auth_header = {'Authorization': f"Bearer {token}"}
    response = requests.post(url, json=payload, headers=auth_header)
    return response

def bulk_upload_staff_district(payload, token):
    url = f"{ENV_HOST}/classes/district_staff/bulk/"
    auth_header = {'Authorization': f"Bearer {token}"}
    generated_file = generate_csv(payload, STAFF_BULK_PARAMS)
    response = requests.post(url, files=dict(roster=('roster.csv', generated_file)), headers=auth_header)
    return response.json()

def bulk_upload_staff_principal(payload, token, org_id):
    url = f"{ENV_HOST} "
    auth_header = {'Authorization': f"Bearer {token}"}
    generated_file = generate_csv(payload, STAFF_BULK_PARAMS)
    response = requests.post(url, files=dict(roster=('roster.csv', generated_file)), headers=auth_header)
    return response
