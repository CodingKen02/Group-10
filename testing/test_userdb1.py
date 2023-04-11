import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

@pytest.fixture
def db():
    engine = create_engine('sqlite:///sh-user-test.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    Base.metadata.drop_all(engine)
    session.close()

def test_create_user(db):
    user = User(name='John Doe', email='johndoe@example.com', password='password123')
    db.add(user)
    db.commit()
    assert user.id == 1

def test_get_user_by_email(db):
    user = User(name='Jane Doe', email='janedoe@example.com', password='password456')
    db.add(user)
    db.commit()
    result = db.query(User).filter_by(email='janedoe@example.com').first()
    assert result.name == 'Jane Doe'

