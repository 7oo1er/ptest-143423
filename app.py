import os
import re
#from peewee import *
import peewee
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
regex = r"postgres://([\w_]{2,20}):([^@]{2,80})@([^:]{2,80}):5432/([\w_0-9]{2,20})"
match = re.search(regex, DATABASE_URL)
db_user, db_password, db_url, db_base = match[1], match[2], match[3], match[4]
db = peewee.PostgresqlDatabase(user=db_user, database=db_base, password=db_password, host=db_url)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class event_log(BaseModel):
    d_id = peewee.CharField(null=True, unique=True)


try:
    event_log.create_table(safe=True)
    print("MessageLog table created!")
except peewee.OperationalError:
    print("MessageLog table already exists!")

now = datetime.now()
today = now.strftime("%H%M%S")
newrecord = (event_log.insert(d_id=today).execute())

# for cls in globals().values():
#     if type(cls) == BaseModel:
#         try:
#             cls.create_table()
#         except OperationalError as e:
#             print(e)