import pytest
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from SneakerHeadz-db import Base, User, Shoe

@pytest.fixture
def session():
    engine = create_engine('sqlite:///sh-database.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_create_user(session):
    user = User(name='John Doe', email='johndoe@example.com', password='password123')
    session.add(user)
    session.commit()
    assert user.id == 1

def test_get_user_by_email(session):
    user = User(name='Jane Doe', email='janedoe@example.com', password='password456')
    session.add(user)
    session.commit()
    result = session.query(User).filter_by(email='janedoe@example.com').first()
    assert result.name == 'Jane Doe'

def test_shoe_model():
    assert Shoe.__tablename__ == 'shoes'
    assert isinstance(Shoe.id.property, Column)
    assert isinstance(Shoe.name.property, Column)
    assert isinstance(Shoe.brand.property, Column)
    assert isinstance(Shoe.price.property, Column)
    assert isinstance(Shoe.user_id.property, Column)

def test_add_shoe(session):
    shoe = Shoe(name='Air Max', brand='Nike', price=200.0)
    session.add(shoe)
    session.commit()
    assert session.query(Shoe).filter_by(name='Air Max').first()

def test_query_shoes(session):
    shoes = session.query(Shoe).all()
    assert len(shoes) > 0
