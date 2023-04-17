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

from sqlalchemy.engine import Engine
from sqlalchemy import event



## Login/Logout/Registration Testing ##


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


## Since user is already existing in the database, user gets returned to the registration page.
def test_user_registration():
    client = app.test_client()
    response = client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    assert response.status_code == 200
    assert response.data == b'Email already Present'

## If User logins correctly, then the user should be redirected to the home page.
def test_user_login():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

## If User logins correctly, then the user should be redirected to the home page.
def test_user_incorrect_login():
    client = app.test_client()
    response = client.post('/login', data={'email': 'bigboy@gmail.com', 'password': '1'})
    assert response.status_code == 200

## Testing account page access
def test_user_account_after_login():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        response = client.get('/account')
        assert response.status_code == 200

## Testing account Logout
def test_logout():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        response = client.get('/account')
        assert response.status_code == 200
    
    response = client.get('/logout')
    assert response.status_code == 302

