import click
import os
import logging
from application.services.authenticate import authenticate
from application.services.create_user import create_staff, bulk_upload_staff_principal, create_student, create_school, bulk_upload_staff_district
from application.seed_gp.user_factory import generate_users, generate_schools
from application.settings import USERNAME, PASSWORD, ENVIRONMENTS

logger = logging.getLogger('__name__')

@click.command()
@click.option('--environment', default="staging", help='Environment to seed (Dev, Staging, etc)')
@click.option('--school_count', default=500, help='Amount of users to create')
def seed_schools(environment, school_count):
    """
    Seed schools with mock data
    """
    environment_url = ENVIRONMENTS[environment]['host']
    auth_token = authenticate(USERNAME, PASSWORD)
    total_ran = 0
    items = generate_schools(school_count)

    for item in items:
        item_json = item.__dict__
        response = create_school(item_json, auth_token)
        if response.status_code == 401:
            auth_token = authenticate(USERNAME, PASSWORD)
            click.echo(f'Whoops Token expired or auth issue, trying again')
            response = create_school(item_json, auth_token)
        click.echo(f'Iteration {item}.  Result: {response.content}')
        total_ran += 1
        click.echo(f'Ran {total_ran}.  Left: {school_count - total_ran}')

    click.echo(f'Process complete')

@click.command()
@click.option('--environment', default="local", help='Environment to seed (Dev, Staging, etc)')
@click.option('--user_count', default=100, help='Amount of users to create')
@click.option('--org_id', default=1222, help='Organization Id to associate User with')
def seed_org_users(environment, user_count, org_id):
    """
    Seed Org Staff with mock data
    """
    environment_url = ENVIRONMENTS[environment]['host']
    auth_token = authenticate(USERNAME, PASSWORD)
    users = generate_users(user_count)
    response = bulk_upload_staff_district(users, auth_token, org_id)

    click.echo(f'Process Response: {response.content}')
    click.echo(f'Process complete')

@click.command()
@click.option('--environment', default="local", help='Environment to seed (Dev, Staging, etc)')
@click.option('--user_count', default=2900, help='Amount of users to create')
@click.option('--increment_amount', default=5, help='Amount to create at a time')
def seed_district_users_bulk(environment, user_count, increment_amount):
    """
    Seed District Staff with mock data and random roles
    """
    environment_url = ENVIRONMENTS[environment]['host']
    auth_token = authenticate(USERNAME, PASSWORD)
    iterations = int(user_count / increment_amount)
    # Range of Staff Roles that a District would use instead of assigning them all
    # as default "Teacher"
    staff_start_id = 25 
    staff_end_id = 42
    staff_current_id = staff_start_id

    total_ran = 0

    for iteration in range(iterations):
        users = generate_users(increment_amount, staff_current_id)
        staff_current_id += 1
        if staff_current_id > staff_end_id:
            staff_current_id = staff_start_id

        response = bulk_upload_staff_district(users, auth_token)
        if response.status_code == 401:
            auth_token = authenticate(USERNAME, PASSWORD)
            click.echo(f'Whoops Token expired or auth issue, trying again')
            response = bulk_upload_staff_district(users, auth_token)
        total_ran += increment_amount
        total_left = user_count - total_ran
        click.echo(f'Iteration {iteration}.  Result: {response.content}')
        click.echo(f'Total Ran: {total_ran} Total Left: {total_left}')

    click.echo(f'Process complete')

@click.command()
@click.option('--environment', default="local", help='Environment to seed (Dev, Staging, etc)')
@click.option('--user_count', default=30000, help='Amount of users to create')
@click.option('--org_id', default=1224, help='Organization Id to associate User with')
def seed_students(environment, user_count, org_id):
    """
    Seed Students with mock data under multiple schools and multiple parents
    """
    environment_url = ENVIRONMENTS[environment]['host']
    auth_token = authenticate(USERNAME, PASSWORD)
    users = generate_users(user_count)
    total_ran = 0

    school_begin = 373  # Refactor to make endpoint to GET all schools in above district
    school_end = 816 
    school_curr = school_begin

    parent_begin = 539741

    for user in users:
        if total_ran % 20 == 0:
            click.echo(f'Creating Parent - Total Ran {total_ran}')
            users = generate_users(2, 4, "Parent")
            parent_json = users[0].__dict__ 
            parent_response = create_staff(parent_json, auth_token, school_curr)
            parent_begin = parent_begin + total_ran + 1

        user_json = user.__dict__
        user_json["parent_id"] = [parent_begin]
        response = create_student(user_json, auth_token, school_curr)
        if response.status_code == 401:
            auth_token = authenticate(USERNAME, PASSWORD)
            click.echo(f'Whoops Token expired or auth issue, trying again')
            response = create_student(user_json, auth_token, school_curr)
    
        click.echo(f'Iteration {user}.  Result: {response.content}')
        total_ran += 1
        school_curr += 1
        if school_curr > school_end:
            school_curr = school_begin
        click.echo(f'Ran {total_ran}.  Left: {user_count - total_ran} School Id: {school_curr}')

    click.echo(f'Process complete')

if __name__ == '__main__':
    seed_district_users_bulk()
    # seed_org_users()
    # seed_students()
    # seed_schools()