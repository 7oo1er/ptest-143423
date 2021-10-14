import re
from peewee import *

load_dotenv()
regex = r"postgres://([\w_]{2,20}):([^@]{2,80})@([^:]{2,80}):5432/([\w_]{2,20})"
match = re.search(regex, DATABASE_URL)
db_user, db_password, db_url, db_base = match[1], match[2], match[3], match[4]
db = PostgresqlDatabase(user=db_user, database=db_base, password=db_password, host=db_url)


class BaseModel(Model):
    class Meta:
        database = db


class event_log(BaseModel):
    d_id = CharField(null=True, unique=True)


try:
    event_log.create_table()
    print("MessageLog table created!")
except peewee.OperationalError:
    print("MessageLog table already exists!")


for cls in globals().values():
    if type(cls) == peewee.BaseModel:
        try:
            cls.create_table()
        except peewee.OperationalError as e:
            print(e)