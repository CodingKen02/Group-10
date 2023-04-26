import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
    brand = Column(String)
    shoetype = Column(String)
    size = Column(Integer)
    condition = Column(String)
    description = Column(String)
    price = Column(Integer)
    picture_filename = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, backref='shoes')

    def __repr__(self):
        return f"<Shoe(brand='{self.brand}', shoetype='{self.shoetype}', size='{self.size}', condition='{self.condition}', description='{self.description}', price='{self.price}', picture_filename='{self.picture_filename}', user='{self.user}')>"

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session
session = Session()

# Add the users to the session
session.add_all()

# Add the shoes to the session
session.add_all()

# Commit the changes to the database
session.commit()
