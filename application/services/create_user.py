import requests
import logging
from jmespath import search
from application.utils.csv import generate_csv
from application.settings import (ENV_HOST, STAFF_BULK_PARAMS)
logger = logging.getLogger(__name__)


def log_upload(payload):
    for line in payload.split('\n'):
        logging.debug(f'Payload row: {line}\n')

def create_staff(payload, token, org_id):
    # maybe should go to a different URL
    url = f"{ENV_HOST}/classes/organization/{org_id}/staff/"
    auth_header = {'Authorization': f"Bearer {token}"}
    response = requests.post(url, json=payload, headers=auth_header)
    return response

def create_school(payload, token):
    url = f"{ENV_HOST}/classes/organization/"
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
    logger.debug(f'Writting users:')
    log_upload(generated_file)
    response = requests.post(url, files=dict(roster=('roster.csv', generated_file)), headers=auth_header)
    return response

def bulk_upload_staff_principal(payload, token, org_id):
    url = f"{ENV_HOST} "
    auth_header = {'Authorization': f"Bearer {token}"}
    generated_file = generate_csv(payload, STAFF_BULK_PARAMS)
    logger.debug(f'Writting users:')
    log_upload(generated_file)
    response = requests.post(url, files=dict(roster=('roster.csv', generated_file)), headers=auth_header)
    return response
