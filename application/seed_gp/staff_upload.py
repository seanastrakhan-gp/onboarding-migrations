import click
import os
import logging
from application.utils.csv import parse_bulk_file
from application.settings import STAFF_BULK_PARAMS
from application.services.authenticate import authenticate, get_role
from application.services.create_user import (
    bulk_upload_staff_district, bulk_upload_staff_principal)
from application.seed_gp.user_factory import generate_users
from application.settings import USERNAME, PASSWORD


logger = logging.getLogger(__name__)

@click.command()
@click.option('--fake_users', default=0, help='Amount of users to create')
@click.option('--org_id', default=1, help='Organization Id to associate User with')
#@click.option('--chunk_size', default=10, help='Bulk upload items size')
@click.option('--bulk_file', default=None, help='Path to bulk upload file')
def seed_staff(fake_users, org_id, bulk_file=None, **kwargs):
    """
    Seed Staff with mock data
    """
    auth_token = authenticate(USERNAME, PASSWORD)
    users = []

    # generating fake users
    fake_users = generate_users(fake_users)
    if fake_users:
        users += fake_users
    logger.debug('Start staff upload')
    if bulk_file:
        bulk_users = parse_bulk_file(file=bulk_file, fields=STAFF_BULK_PARAMS)
        if bulk_users:
            users += bulk_users

    # getting user_role
    role = get_role(auth_token)

    # define method by user role
    if role == 'district':
        data = bulk_upload_staff_district(users, auth_token)
    elif role == 'principal':
        data = bulk_upload_staff_principal(users, auth_token, org_id)
    else:
        logger.error('User should be district or principal')
        return
    logger.debug('Staff list added to the system')
    success_count = data.get('count')
    click.echo(f'{success_count} of {len(users)} users created')
    click.echo(f'Process complete')
    logger.debug('Finished staff upload')


if __name__ == '__main__':
    seed_staff()