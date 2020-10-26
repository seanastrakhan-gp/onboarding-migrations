import click
import os
import logging
from application.utils.csv import parse_bulk_file
from application.settings import STAFF_BULK_PARAMS
from application.services.api import set_new_auth
from application.services.api import get_role
from application.services.create_user import (
    bulk_upload_staff_district, bulk_upload_staff_principal)
from application.seed_gp.user_factory import generate_staff
from application.settings import USERNAME, PASSWORD

logger = logging.getLogger(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@click.command()
@click.option('--fake_users', default=2, help='Amount of users to create')
@click.option('--org_id', default=1, help='Organization Id to associate User with')
@click.option('--bulk_file_name', default='test.csv', help='Path to bulk upload file')
def seed_staff_from_file(fake_users, org_id, bulk_file_name, **kwargs):
    """
    Migrate Staff data from file
    """
    file_path = f"{ROOT_DIR}/data_sources/{bulk_file_name}"
    auth_token = authenticate(USERNAME, PASSWORD)
    users = []
    set_new_auth()

    logger.debug('Start staff upload')
    if bulk_file_name:
        bulk_users = parse_bulk_file(file=file_path, fields=STAFF_BULK_PARAMS)
        if bulk_users:
            users += bulk_users
    else:
        raise Exception('Bulk file Missing')

    # getting user_role
    role = get_role()

    # define method by user role and rerun if expired
    if role == 'district':
        data = bulk_upload_staff_district(users)
    elif role == 'principal':
        data = bulk_upload_staff_principal(users, org_id)
    else:
        logger.error('User should be district or principal')
        return
    if response.status_code == 200:
        success_count = response.json().get('count')
        click.echo(f'{success_count} of {len(users)} users created.')
    else:
        click.echo(f'Error creating Users: {response.content}')


if __name__ == '__main__':
    seed_staff_from_file()