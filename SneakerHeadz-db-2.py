# Import necessary modules
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the engine for the user database
user_engine = create_engine('sqlite:///sh-user.db', echo=True)

# Create the engine for the inventory database
inventory_engine = create_engine('sqlite:///sh-inventory.db', echo=True)

# Create a session factory for each database
UserSession = sessionmaker(bind=user_engine)
InventorySession = sessionmaker(bind=inventory_engine)

# Define the base class for each database
UserBase = sqlalchemy.orm.declarative_base(bind=user_engine)
InventoryBase = sqlalchemy.orm.declarative_base(bind=inventory_engine)

# Define the User model for the user database
class User(UserBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

# Define the Shoe model for the inventory database
class Shoe(InventoryBase):
    __tablename__ = 'shoes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='shoes')
    
    def __repr__(self):
        return f"<Shoe(name='{self.name}', brand='{self.brand}', price={self.price}, user_id='{self.user_id}')>"

# Create the tables in each database
UserBase.metadata.create_all(user_engine)
InventoryBase.metadata.create_all(inventory_engine)

# Create a session object for each database
user_session = UserSession()
inventory_session = InventorySession()

# Create some example users
user1 = User(name='Alice', email='alice@example.com')
user2 = User(name='Bob', email='bob@example.com')
user3 = User(name='Charlie', email='charlie@example.com')
user_session.add_all([user1, user2, user3])
user_session.commit()

# Create some example shoes linked to users
shoe1 = Shoe(name='Air Max 90', brand='Nike', price=120.00, user=user1)
shoe2 = Shoe(name='Yeezy Boost 350 V2', brand='Adidas', price=220.00, user=user2)
shoe3 = Shoe(name='Retro 1 High OG', brand='Jordan', price=150.00, user=user3)
shoe4 = Shoe(name='Chuck Taylor All Star', brand='Converse', price=50.00, user=user1)
shoe5 = Shoe(name='Classic Slip-On', brand='Vans', price=60.00, user=user2)
shoe6 = Shoe(name='Superstar', brand='Adidas', price=80.00, user=user3)
inventory_session.add_all([shoe1, shoe2, shoe3, shoe4, shoe5, shoe6])
inventory_session.commit()

# Close the sessions
user_session.close()
inventory_session.close()
