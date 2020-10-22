from application.utils.json import parse_json_file

settings_data = parse_json_file('./settings.json')
ENVIRONMENTS = settings_data['environments']
USERNAME = settings_data['username']
PASSWORD = settings_data['password']
ENV = settings_data['env']
ENV_HOST = ENVIRONMENTS[ENV]['host']
