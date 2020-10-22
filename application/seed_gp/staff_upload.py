import click
import os
from application.settings import ENVIRONMENTS
from application.services.authenticate import authenticate, get_role
from application.services.create_user import create_staff, bulk_upload_staff_district, bulk_upload_staff_principal
from .user_factory import generate_users
from application.settings import USERNAME, PASSWORD


@click.command()
@click.option('--user_count', default=56, help='Amount of users to create')
@click.option('--org_id', default=1, help='Organization Id to associate User with')
def seed_staff(user_count, org_id):
    """
    Seed Staff with mock data
    """
    auth_token = authenticate(USERNAME, PASSWORD)
    users = generate_users(user_count)
    role = get_role(auth_token)
    if role == 'district':
        data = bulk_upload_staff_district(users, auth_token)
    else:
        data = bulk_upload_staff_principal(users, auth_token, org_id)
    success_count = data.get('count')
    click.echo(f'{success_count} of {user_count} users created')
    click.echo(f'Process complete')

seed_staff()