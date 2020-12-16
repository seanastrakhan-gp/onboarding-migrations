from application.utils.json import parse_json_file
import logging
import time
import sys
import diskcache as dc

STUDENT_BULK_REGISTRATION_PARAMS = (
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
# logging settings
file_handler = logging.FileHandler(filename=f'logs/{int(time.time())}.log')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
handlers = [file_handler, stdout_handler]
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, handlers=handlers)

# initialize cache
cache = dc.Cache('tmp')



settings_data = parse_json_file('./settings.json')
ENVIRONMENTS = settings_data['environments']
USERNAME = settings_data['username']
PASSWORD = settings_data['password']
ENV = settings_data['env']
ENV_HOST = ENVIRONMENTS[ENV]['host']