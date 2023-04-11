import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a database engine
engine = create_engine('sqlite:///sh-inventory.db', echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)

# Define the database schema
Base = sqlalchemy.orm.declarative_base()

# Define the Shoe model
class Shoe(Base):
    __tablename__ = 'shoes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    def __repr__(self):
        return f"<Shoe(name='{self.name}', brand='{self.brand}', price={self.price}, user_id='{self.user_id}')>"


# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session object
session = Session()

# Create some example shoes
shoe1 = Shoe(name='Air Max 90', brand='Nike', price=120.00, user_id=1)
shoe2 = Shoe(name='Yeezy Boost 350 V2', brand='Adidas', price=220.00, user_id=2)
shoe3 = Shoe(name='Retro 1 High OG', brand='Jordan', price=150.00, user_id=3)
shoe4 = Shoe(name='Chuck Taylor All Star', brand='Converse', price=50.00, user_id=1)
shoe5 = Shoe(name='Classic Slip-On', brand='Vans', price=60.00, user_id=2)
shoe6 = Shoe(name='Superstar', brand='Adidas', price=80.00, user_id=3)
session.add_all([shoe1, shoe2, shoe3, shoe4, shoe5, shoe6])
session.commit()

# Close the session
session.close()