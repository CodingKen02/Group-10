# from flask import session

# def test_userlogin(client):
#     response = client.get('/login')
#     assert b'Login' in response.data

# def test_valid_login(client):
#     response = client.post('/login', data=dict(
#         username='example',
#         password='password'
#     ), follow_redirects=True)
#     assert b'Welcome' in response.data
#     assert session['username'] == 'example'

# def test_invalid_login(client):
#     response = client.post('/login', data=dict(
#         username='foo',
#         password='bar'
#     ), follow_redirects=True)
#     assert b'Invalid username or password' in response.data
#     assert 'username' not in session

# def test_logout(client):
#     with client.session_transaction() as sess:
#         sess['username'] = 'example'

#     response = client.get('/logout', follow_redirects=True)
#     assert b'Login' in response.data
#     assert 'username' not in session

# def test_home(client):
#     with client.session_transaction() as sess:
#         sess['username'] = 'example'

#     response = client.get('/')
#     assert b'Welcome' in response.data

# def test_unauthorized_access(client):
#     response = client.get('/')
#     assert response.status_code == 302
#     assert response.location.endswith('/login')

