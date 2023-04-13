from flask import session

def test_login(client):
    # test if login is successful
    response = client.post('/login', data={'username': 'seller', 'password': 'password'})
    assert response.status_code == 302  # check if page redirects to dashboard
    assert session.get('seller') is True  # check if seller session is created

def test_invalid_login(client):
    # test if invalid login credentials are rejected
    response = client.post('/login', data={'username': 'invalid', 'password': 'invalid'})
    assert response.status_code == 200  # check if error message is displayed

def test_dashboard(client):
    # test if dashboard is only accessible to logged-in seller
    response = client.get('/dashboard')
    assert response.status_code == 302  # check if page redirects to login

    with client.session_transaction() as sess:
        sess['seller'] = True  # simulate logged-in seller
    response = client.get('/dashboard')
    assert response.status_code == 200  # check if dashboard is displayed

def test_logout(client):
    # test if seller session is ended after logging out
    with client.session_transaction() as sess:
        sess['seller'] = True  # simulate logged-in seller
    response = client.get('/logout')
    assert response.status_code == 302  # check if page redirects to login
    assert session.get('seller') is None  # check if seller session is ended

