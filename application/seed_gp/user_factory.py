from faker import Faker
from slugify import slugify
from datetime import datetime
import json


faker = Faker()
class School:
  def __init__(self, index, **kwargs):
    self.description = f"School for people who want to be a {faker.job()}"
    self.org_type = kwargs.get("org_type") or 4
    self.country = kwargs.get("country") or "usa"
    self.district = kwargs.get("district")
    self.is_premium = kwargs.get("is_premium") or False 
    self.org_name = kwargs.get("org_name") or f"{faker.name()}-{index}"
    self.phone = kwargs.get("phone") or faker.phone_number()
    self.visibility = kwargs.get("visibility") or "public"

    @property
    def email(self):
      return f"{self.org_name}{datetime.now()}@mailinator.com"

class User:
  faker = Faker()
  def __init__(self, index, **kwargs):
    self.first_name = kwargs.get("first_name") or self.faker.first_name()
    self.last_name = kwargs.get("last_name")  or self.faker.last_name()
    self.index = index
    self.staff_role = kwargs.get("staff_role_id", None)
    self.staff_role_name = kwargs.get("staff_role_name", None)
    self.username = slugify(f"{self.first_name}{datetime.now()}",replacements=[["-", ""]])
  # @property
  # def username(self):
  #   username =  slugify(f"{self.first_name}{datetime.now()}",replacements=[["-", ""]])
  #   return username

  @property
  def password(self):
    password =  "12345678"
    return password

  @property
  def email(self):
    return f"{self.username}@mailinator.com"

def generate_users(count, role=3, role_name="Teacher"):
  users = [User(index, staff_role_id=role, staff_role_name=role_name) for index in range(count)]
  return users

def generate_schools(count):
  schools = [School(index) for index in range(count)]
  return schools