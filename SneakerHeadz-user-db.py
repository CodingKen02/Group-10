import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a database engine
engine = create_engine('sqlite:///sh-user.db', echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)

# Define the database schema
Base = sqlalchemy.orm.declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session object
session = Session()

# Create some example users
user1 = User(name='John', email='john@example.com', password='password1')
user2 = User(name='Jane', email='jane@example.com', password='password2')
user3 = User(name='Bob', email='bob@example.com', password='password3')
session.add_all([user1, user2, user3])
session.commit()

# Close the session
session.close()
