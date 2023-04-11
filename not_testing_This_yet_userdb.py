import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
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
