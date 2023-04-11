import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a database engine
engine = create_engine('sqlite:///sh-inventory.db')

# Create a session factory
Session = sessionmaker(bind=engine)

# Define the database schema
Base = declarative_base()

# Define the Shoe model
class Shoe(Base):
    __tablename__ = 'shoes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f"<Shoe(name='{self.name}', brand='{self.brand}', price={self.price})>"

# Test Shoe model creation
def test_shoe_model():
    assert Shoe.__tablename__ == 'shoes'
    assert isinstance(Shoe.id.property, sqlalchemy.orm.ColumnProperty)
    assert isinstance(Shoe.name.property, sqlalchemy.orm.ColumnProperty)
    assert isinstance(Shoe.brand.property, sqlalchemy.orm.ColumnProperty)
    assert isinstance(Shoe.price.property, sqlalchemy.orm.ColumnProperty)
    assert isinstance(Shoe.user_id.property, sqlalchemy.orm.ColumnProperty)

# Test adding a shoe to the database
def test_add_shoe():
    session = Session()
    shoe = Shoe(name='Air Max', brand='Nike', price=200.0)
    session.add(shoe)
    session.commit()
    assert session.query(Shoe).filter_by(name='Air Max').first()

# Test querying shoes from the database
def test_query_shoes():
    session = Session()
    shoes = session.query(Shoe).all()
    assert len(shoes) > 0

# Create the tables in the database
Base.metadata.create_all(engine)
