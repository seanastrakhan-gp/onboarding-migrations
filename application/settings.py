from application.utils.json import parse_json_file
import logging
import time

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=f'logs/{int(time.time())}.log',
                    level=logging.DEBUG, format=LOG_FORMAT)
settings_data = parse_json_file('./settings.json')
ENVIRONMENTS = settings_data['environments']
USERNAME = settings_data['username']
PASSWORD = settings_data['password']
ENV = settings_data['env']
ENV_HOST = ENVIRONMENTS[ENV]['host']
