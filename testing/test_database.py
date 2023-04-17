import re
from flask import Flask, session, request, render_template
import sys
sys.path.append("source")
sys.path.append("source/instance")
from source.app import app, create_all
from source.models import *

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/accounts.db'

create_all()

## Database testing will test whether or not we can ##
## access the various databases and push/pull data  ##
## in a way that coincides with how the website     ##
## currently works in its beta state.               ##


## Can we access the register, login, logout, and user account pages?
def test_go_to_login():
    response = app.test_client().get('/register.html')
    assert response.status_code == 200


def test_go_to_login():
    response = app.test_client().get('/login')
    assert response.status_code == 200

def test_go_to_logout():
    response = app.test_client().get('/logout.html')
    assert response.status_code == 200

def test_go_to_logout_confirm():
    response = app.test_client().get('/logoutconfirm')
    assert response.status_code == 200

def test_go_to_user_account_page():
    response = app.test_client().get('/account')
    # Not logged in, so should redirect.
    assert response.status_code == 302

## Now lets test functionality
## The accounts.db should have data already.
## Lets test with one of our existing users (myself, Ander)

def test_user_login():
    client = app.test_client()
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})

    assert response.status_code == 200

## Testing account page access
def test_user_account_after_login():
    client = app.test_client()
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 200

    with client:
        response = client.get('/account')
        assert response.status_code == 200
