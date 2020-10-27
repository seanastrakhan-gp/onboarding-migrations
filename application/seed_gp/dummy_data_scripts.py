import click
import os
import logging
import asyncio
import time
from application.services.authenticate import authenticate
from application.services.create_user import create_staff, bulk_upload_staff_principal, \
create_student, create_school, bulk_upload_staff_district, bulk_upload_students
from application.services.crete_user_async import post_async_student, test_async, process_users
from application.seed_gp.user_factory import generate_users, generate_schools
from application.settings import USERNAME, PASSWORD, ENVIRONMENTS
from application.utils.csv import parse_bulk_file
from application.utils.chunks import chunks

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


async def print_when_done(tasks):
    for res in asyncio.as_completed(tasks):
        print(f"Result {await res}")

@click.command()
@click.option('--environment', default="local", help='Environment to seed (Dev, Staging, etc)')
@click.option('--user_count', default=10, help='Amount of users to create')
@click.option('--org_id', default=1224, help='Organization Id to associate User with')
@click.option('--chunk_size', default=5, help='Bulk upload items size')

def seed_students(environment, user_count, org_id, chunk_size):
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

    [setattr(student,'parent_id',[parent_begin]) for student in users]
    users = [student.__dict__ for student in users]
    index = 0 

    start = time.perf_counter()
    while index < len(users):
        ## Sync Run
        # response = create_student(users[index], school_curr, index)
        # print('Response content', response)
        # index += 1

        users_to_upload = users[index: index + chunk_size]

        ## Async standard
        #coros = [create_student(users[i], school_curr, i) for i in range(index, index + chunk_size)]
        # asyncio.get_event_loop().run_until_complete(test_async(school_curr, auth_token, users_to_upload, index))

        # async gather
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process_users(users_to_upload, school_curr, auth_token, index))
        # Async Futures
        # futures = []
        # for u in users_to_upload:
        #     futures.append(post_async_student(school_curr, auth_token, u, index))   
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(asyncio.wait(futures))
        
        index += chunk_size

        school_curr += 1
        if school_curr > school_end:
            school_curr = school_begin
        click.echo(f'Loop {index} done')
    loop.close()
    end = time.perf_counter() - start

    click.echo(f'Process complete (took {end:0.2f} seconds)')


    # for user in users:
    #     # if total_ran % 20 == 0:
    #     #     click.echo(f'Creating Parent - Total Ran {total_ran}')
    #     #     users = generate_users(2, 4, "Parent")
    #     #     parent_json = users[0].__dict__ 
    #     #     parent_response = create_staff(parent_json, auth_token, school_curr)
    #     #     parent_begin = parent_begin + total_ran + 1

    #     user_json = user.__dict__
    #     user_json["parent_id"] = [parent_begin]
    #     group1 = create_student(user_json, auth_token, school_curr)
    #     coros = [create_student(user_json, auth_token, school_curr)


    #     several_futures = asyncio.gather(
    #         mycoro(1), mycoro(2), mycoro(3))

    #     # response = create_student(user_json, auth_token, school_curr)
    
    #     click.echo(f'Iteration {user}.  Result: {response.content}')
    #     total_ran += 1
    #     school_curr += 1
    #     if school_curr > school_end:
    #         school_curr = school_begin
    #     click.echo(f'Ran {total_ran}.  Left: {user_count - total_ran} School Id: {school_curr}')

    # click.echo(f'Process complete')

if __name__ == '__main__':
    # seed_district_users_bulk()
    # seed_org_users()
    seed_students()
    # seed_schools()