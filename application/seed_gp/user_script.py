import click
import os
from settings import ENVIRONMENTS
from application.services.authenticate import authenticate
from application.services.create_user import create_staff
from .user_factory import generate_users
from application.settings import USERNAME, PASSWORD


@click.command()
@click.option('--environment', default="local", help='Environment to seed (Dev, Staging, etc)')
@click.option('--user_count', default=56, help='Amount of users to create')
@click.option('--org_id', default=1, help='Organization Id to associate User with')
def seed_users(environment, user_count, org_id):
    """
    Seed Staff with mock data
    """
    environment_url = ENVIRONMENTS[environment]['host']
    auth_token = authenticate(USERNAME, PASSWORD)
    users = generate_users(user_count)

    for user in users:
        json_payload = user.__dict__
        result = create_staff(json_payload, auth_token, environment_url, org_id)
        # Figure out what needs to happen above so user creation 
        click.echo(f'Result: {result}')
    click.echo(f'Process complete')

if __name__ == '__main__':
    seed_users()