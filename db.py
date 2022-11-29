import datetime
import random

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, BIGINT, Date, BigInteger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

# Creating Role Class for SQLAlchemy Table
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


# Creating User Class for SQLAlchemy Table
class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    fio = Column(Text)
    datar = Column(Date)
    id_role = Column(Integer, ForeignKey('roles.id'))
    role = relationship(Role, backref='users', lazy='subquery')


# Create Session
session_maker = sessionmaker(bind=create_engine('sqlite:///chatBot.db'))


# Add user to DB
def db_table_add_user(fio: str,):
    with session_maker() as session:
        date1, date2 = datetime.date(1950, 1, 1), datetime.date(2022, 1, 1) # Date1 - start date for random, Date2 - end date for random
        datar = random_date(date1, date2)  # Randomizing Dates
        id_role = random.randint(1, 2)  # Randomizong Roles

        # Adding User to DataBase
        user = User(fio=fio, datar=datar, id_role=id_role)

        session.add(user)
        session.commit()


# Randomizing Date Function
def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


# Get last 5 users from DataBase
def return_users():
    users_arr = []

    with session_maker() as session:
        user_records = session.query(User).order_by(User.id.desc()).limit(5)

        for user in user_records:
            users_arr.append(user)

        return users_arr
