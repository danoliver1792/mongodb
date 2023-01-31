from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer, String, ForeignKey

# integration (base class for declarative class definitions)
Base = declarative_base()

# getting class by inheritance
class User(Base):
    __tablename__ = "User"
    # attributes
    id = Column(Integer, primary_key=True, auto_increment=True)
    name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)

    # defining the relationship
    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, last_name={self.last_name})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, auto_increment=True)
    email_address = Column(String(100), nullable=False)  # nullable = NOT NULL
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship(
        "User", back_populates="address"
    )

    def __repr__(self):
        return f"Address(id={self.id}, email={self.email_address})"


print(User.__tablename__)
print(Address.__tablename__)

# database connection
engine = create_engine("sqlite://")

# creating the classes as a table in the database
Base.metadata.create_all(engine)

print(engine.table_names())

# inspector for information - performs database schema inspection
inspector_engine = inspect(engine)
print(inspector_engine.has_table("user_account"))  # True

# table names
print(inspector_engine.get_tables_names())

# creating and working with sessions
with Session(engine) as session:
    danrlei = User(
        name='Danrlei',
        last_name='Danrlei Oliveira',
        address=[Address(email_address='danrlei.jesus@hotmail.com')]
    )

    sandy = User(
        name='Sandy',
        last_name='Sandy Oliveira',
        address=[Address(email_address='sandy.oliveira@gmail.com'),
                 Address(email_address='sandyoliveira12@hotmail.com')]
    )

    patrick = User(
        name='Patrick',
        last_name='Patrick Vieira',
    )

    # sending to the database
    session.add_all([danrlei, sandy, patrick])

    session.commit()

# database queries
stmt = select(User).where(User.name.in_(["danrlei", "sandy"]))
for user in session.scalars(stmt):
    print(user)

stmt_order = select(User).order_by(User.last_name.desc())
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(User.last_name, Address.email_address).join_from(Address, User)
for result in session.scalars(stmt_join):
    print(result)

# checking queries
print(select(User.last_name, Address.email_address).join_from(Address, User))

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(User)
for result in session.scalars(stmt_count):
    print(result)
