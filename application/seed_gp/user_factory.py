import time
from faker import Faker
import json


class User:
  DEFAULT_PASSWORD = '12345678'
  faker = Faker()

  def __init__(self, index, **kwargs):
    # index should be first
    self.index = str(int(time.time()))
    self.first_name = kwargs.get("first_name") or self.faker.first_name()
    self.last_name = kwargs.get("last_name") or self.faker.last_name()
    self.staff_role = kwargs.get("staff_role_id", None)
    self.username = kwargs.get("username") or self.gen_user_name()
    self.password = kwargs.get("password") or self.DEFAULT_PASSWORD
    self.email = self.gen_email()

  def gen_user_name(self):
    generated_firstname = self.first_name.replace(' ', '_').lower()
    return f'{generated_firstname}{self.index}'


  def gen_email(self):
    return f"{self.first_name}{self.index}@mailinator.com"



def generate_staff(count):
    TEACHER_GROUP_ID = 3
    users = [User(index, staff_role_id=TEACHER_GROUP_ID).__dict__ for index in range(count)]
    return users

def generate_students(count):
    users = [User(index).__dict__ for index in range(count)]
    return users
