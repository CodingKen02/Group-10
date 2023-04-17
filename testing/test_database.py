import re
import pytest
from flask import Flask, session, request, render_template
from flask_login import login_user, logout_user
import sys
import os
import tempfile
sys.path.append("source")
sys.path.append("source/instance")
from source.app import app
from source.models import *
from source.instance import *


@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True
    
    with app.app.app_context():
        app.db.create_all()
        
    yield app.db
    
    app.db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)


## Database testing will test whether or not we can ##
## access the various databases and push/pull data  ##
## in a way that coincides with how the website     ##
## currently works in its beta state.               ##


## Can we access the register, login, logout, and user account pages?
def test_go_to_login():
    response = app.get('/register.html')
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
    response = app.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

## Testing account page accessS
def test_user_account_after_login():
    client = app.test_client()
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        # Log in user before making GET request to /account
        user = User.query.filter_by(email='andertalley@gmail.com').first()
        login_user(user)

        response = client.get('/account')
        assert response.status_code == 200
