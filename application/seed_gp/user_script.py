import click
import os
from constants import environment_urls
from application.services.authenticate import authenticate
from application.services.create_user import create_user
from user_factory import generate_users

@click.command()
@click.option('--environment', default="local", help='Environment to seed (Dev, Staging, etc)')
@click.option('--user_count', default=56, help='Amount of users to create')
@click.option('--org_id', default=1, help='Organization Id to associate User with')
def seed_users(environment, user_count, org_id):
    """
    Seed Staff with mock data
    """
    username = "PTA_Demo" # os.environ.get('USERNAME')
    password = "PTA_Demo" # os.environ.get('PASSWORD')
    environment_url = environment_urls.get(environment)
    auth_token = authenticate(username, password, environment_url)
    users = generate_users(user_count)

    for user in users:
        json_payload = user.__dict__
        result = create_user(json_payload, auth_token, environment_url, org_id)
        # Figure out what needs to happen above so user creation 
        click.echo(f'Result: {result}')

    click.echo(f'Process complete')

if __name__ == '__main__':
    seed_users()