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
    #TODO - I don't think this line below is working
    return f"{self.first_name}{index}@mailinator.com"

def generate_users(count):
  TEACHER_GROUP_ID = 3
  users = [User(index, staff_role_id=TEACHER_GROUP_ID) for index in range(count)]
  return users