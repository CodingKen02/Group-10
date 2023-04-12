import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a database engine
engine = create_engine('sqlite:///sh-database.db', echo=True)

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
        return f"<Shoe(name='{self.name}', brand='{self.brand}', price={self.price}, user='{self.user_id}')>"

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session
session = Session()

# Create some users
user1 = User(name='John', username='john123', password='password1')
user2 = User(name='Jane', username='jane456', password='password2')

# Add the users to the session
session.add_all([user1, user2])

# Create some shoes
shoe1 = Shoe(name='Nike Air Max', brand='Nike', price=100, user=user1)
shoe2 = Shoe(name='Adidas Ultraboost', brand='Adidas', price=120, user=user2)
shoe3 = Shoe(name='Vans Old Skool', brand='Vans', price=50, user=user2)

# Add the shoes to the session
session.add_all([shoe1, shoe2, shoe3])

# Commit the changes to the database
session.commit()
