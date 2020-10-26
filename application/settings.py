from application.utils.json import parse_json_file
import logging
import time

STUDENT_BULK_REGISTRATION_PARAMS = (
    'id',
    'first_name',
    'last_name',
    'birthdate',
    'gender',
    'address',
    'address_2',
    'city',
    'zipcode',
    'country',
)

STAFF_BULK_PARAMS = (
    'first_name',
    'last_name',
    'username',
    'password',
    'email',
    'mobile',
    'staff_role_name',
    'staff_role'
)

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=f'logs/{int(time.time())}.log',
                    level=logging.DEBUG, format=LOG_FORMAT)
settings_data = parse_json_file('./settings.json')
ENVIRONMENTS = settings_data['environments']
USERNAME = settings_data['username']
PASSWORD = settings_data['password']
ENV = settings_data['env']
ENV_HOST = ENVIRONMENTS[ENV]['host']