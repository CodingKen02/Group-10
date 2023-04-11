import pytest
from flask import url_for
from app import app, db, Account


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client
    with app.app_context():
        db.drop_all()


def test_create_account(client):
    response = client.post('/create_account', data={
        'username': 'testuser',
        'password': 'testpassword',
        'account_type': 'Consumer'
    })
    assert response.status_code == 200
    assert b'Account created successfully!' in response.data

    account = Account.query.filter_by(username='testuser').first()
    assert account is not None
    assert account.password == 'testpassword'
    assert account.account_type == 'Consumer'


def test_create_account_missing_fields(client):
    response = client.post('/create_account', data={
        'username': '',
        'password': '',
        'account_type': ''
    })
    assert response.status_code == 200
    assert b'Please fill in all required fields.' in response.data

    account = Account.query.filter_by(username='').first()
    assert account is None


def test_create_account_existing_username(client):
    existing_account = Account(username='existinguser', password='existingpassword', account_type='Consumer')
    db.session.add(existing_account)
    db.session.commit()

    response = client.post('/create_account', data={
        'username': 'existinguser',
        'password': 'newpassword',
        'account_type': 'Seller'
    })
    assert response.status_code == 200
    assert b'That username is already taken.' in response.data

    account = Account.query.filter_by(username='existinguser').first()
    assert account.password == 'existingpassword'
    assert account.account_type == 'Consumer'


def test_create_account_invalid_account_type(client):
    response = client.post('/create_account', data={
        'username': 'testuser',
        'password': 'testpassword',
        'account_type': 'InvalidAccountType'
    })
    assert response.status_code == 200
    assert b'Invalid account type selected.' in response.data

    account = Account.query.filter_by(username='testuser').first()
    assert account is None


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1>Welcome to the Homepage!</h1>' in response.data


def test_create_account_form(client):
    response = client.get('/create_account')
    assert response.status_code == 200
    assert b'<h1>Create Account</h1>' in response.data
