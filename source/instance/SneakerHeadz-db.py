import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

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
        return f"<User(name='{self.name}', email='{self.email}')>"

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
