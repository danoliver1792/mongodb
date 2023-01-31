from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

engine = create_engine('sqlite:///:memory')

# creating schema
metadata_object = MetaData(schema='test')

# creating tables
user = Table(
    "user", metadata_object,
    Column("user_id", Integer, primary_key=True, auto_increment=True),
    Column("user_name", String(100), nullable=False),
    Column("email_address", String(100), nullable=False),
    Column("nickname", String(45), nullable=False)
)

user_prefs = Table(
    "user_prefs", metadata_object,
    Column("pref_id", Integer, primary_key=True, auto_increment=True),
    Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False),
    Column("pref_name", String(45), nullable=False),
    Column("pref_value", String(100))
)


for table in metadata_object.sorted_tables:
    print(table)

# accessing table information
print(user_prefs.primary_key)
print(user_prefs.constraints)

metadata_db_object = MetaData(schema='bank')

financial_info = Table(
    "financial_info", metadata_db_object,
    Column("id", Integer, primary_key=True, auto_increment=True),
    Column("value", String(100), nullable=False)
)

print(financial_info.primary_key)
print(financial_info.foreign_keys)
print(financial_info.constraints)
