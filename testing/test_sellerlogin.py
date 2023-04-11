from app import app
import pytest

@pytest.fixture
def client():
    client = app.test_client()
    yield client

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Username' in response.data
    assert b'Password' in response.data

def test_valid_login(client):
    response = client.post('/login', data=dict(
        username='seller',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to the seller dashboard!' in response.data

def test_invalid_login(client):
    response = client.post('/login', data=dict(
        username='wrong_username',
        password='wrong_password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid login credentials' in response.data

def test_dashboard_requires_login(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data

def test_logout(client):
    with client.session_transaction() as session:
        session['seller'] = True

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data
