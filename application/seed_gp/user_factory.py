from faker import Faker
from datetime import datetime
import json

class User:
  faker = Faker()
  def __init__(self, index, **kwargs):
    self.first_name = kwargs.get("first_name") or self.faker.first_name()
    self.last_name = kwargs.get("last_name")  or self.faker.last_name()
    self.index = index
    self.staff_role = kwargs.get("staff_role_id", None)
  @property
  def user_name(self):
    return f"{self.first_name}{datetime.now()}"

  @property
  def email(self):
    return f"{self.first_name}{index}@mailanator.com"

  # Convert Object to JSON
  def toJSON(self):
      return json.dumps(self, default=lambda o: o.__dict__, 
          sort_keys=True, indent=4)

def generate_users(count):
  users = [User(index) for index in range(count)]
  return users