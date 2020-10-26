import click
import logging
from application.utils.csv import parse_bulk_file
from application.utils.chunks import chunks
from application.services.api import set_new_auth
from application.settings import STAFF_BULK_PARAMS
from application.services.create_user import bulk_upload_students
from application.seed_gp.user_factory import generate_students


logger = logging.getLogger('students_upload')

@click.command()
@click.option('--fake_users', default=0, help='Amount of students to create')
@click.option('--org_id', default=1, help='Organization Id to associate User with')
@click.option('--chunk_size', default=100, help='Bulk upload items size')
@click.option('--bulk_file', default=None, help='Path to bulk upload file')
def seed_students(fake_users, org_id, bulk_file=None, chunk_size=None, **kwargs):
    """
    Seed Students with mock data
    """
    users = []
    set_new_auth()
    success_count = 0
    # generating fake users
    fake_users = generate_students(fake_users)
    if fake_users:
        users += fake_users
    logger.info('Start students upload')
    if bulk_file:
        bulk_users = parse_bulk_file(file=bulk_file, fields=STAFF_BULK_PARAMS)
        if bulk_users:
            users += bulk_users

    users_count = len(users)

    # make progress more clear use bulk upload by chunks
    for chunk_num, chunk in chunks(users, chunk_size):
        start = chunk_num+1
        end = start + chunk_size
        logger.info(f'Writing users {start} to {end} of {users_count}')
        data = bulk_upload_students(chunk, org_id)
        success_count += data and len(data) or 0

    logger.info(f'{success_count} of {users_count} users created')


if __name__ == '__main__':
    seed_students()