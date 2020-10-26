import requests
import logging
from jmespath import search
from application.utils.csv import generate_csv
from application.settings import (ENV_HOST, STAFF_BULK_PARAMS,
                                  STUDENT_BULK_REGISTRATION_PARAMS)
from application.services.api import authorized_request
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


def create_student(payload, token, org_id):
    url = f"{ENV_HOST}/classes/organization/{org_id}/student_user/"
    auth_header = {'Authorization': f"Bearer {token}"}
    response = requests.post(url, json=payload, headers=auth_header)
    return response


def bulk_upload_staff_district(payload, token):
    url = f"{ENV_HOST}/classes/district_staff/bulk/"
    generated_file = generate_csv(payload, STAFF_BULK_PARAMS)
    logger.debug(f'Writing users:')
    log_upload(generated_file)
    response = authorized_request('post', url, files=dict(
        roster=('roster.csv', generated_file)))
    return response


def bulk_upload_staff_principal(payload, token, org_id):
    url = f"{ENV_HOST}"
    generated_file = generate_csv(payload, STAFF_BULK_PARAMS)
    logger.debug(f'Writing users:')
    log_upload(generated_file)
    response = authorized_request('post', url, files=dict(
        roster=('roster.csv', generated_file)))
    return response


def bulk_upload_students(payload, org_id):
    url = f'{ENV_HOST}/classes/organization/{org_id}/students/bulk/'
    generated_file = generate_csv(payload, STUDENT_BULK_REGISTRATION_PARAMS)
    logger.debug(f'Writing users:')
    log_upload(generated_file)
    response = authorized_request('post', url, files=dict(
        roster=('roster.csv', generated_file)))
    return response.json()

