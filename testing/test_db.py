import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest

# Create a database engine
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)

# Define the database schema
Base = sqlalchemy.orm.declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', username='{self.username}')>"

# Define the Shoe model
class Shoe(Base):
    __tablename__ = 'shoes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    price = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, backref='shoes')

    def __repr__(self):
        return f"<Shoe(name='{self.name}', brand='{self.brand}', price={self.price})>"

# Create the tables in the database
Base.metadata.create_all(engine)

@pytest.fixture(scope="module")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_create_user(db_session):
    user = User(name='John', username='johndoe', password='password')
    db_session.add(user)
    db_session.commit()
    assert user.id is not None

def test_create_shoe(db_session):
    user = User(name='John', username='johndoe', password='password')
    db_session.add(user)
    db_session.commit()
    shoe = Shoe(name='Sneakers', brand='Nike', price=100, user_id=user.id)
    db_session.add(shoe)
    db_session.commit()
    assert shoe.id is not None
