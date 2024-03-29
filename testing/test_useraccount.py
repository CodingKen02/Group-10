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




## This will test our useraccount page ##


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


## User Logs in, then navigates to their account page.
def test_user_account_after_login():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        response = client.get('/account')
        assert response.status_code == 200

## User has multiple options depending on what button they hit for their Account Page.
## Lets go through them in order and corresponding to what we currently have running.

## Logout:
## Testing account Logout
def test_logout():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        response = client.get('/account')
        assert response.status_code == 200
    
    # goes to logoutconfirm.html
    response = client.get('/logout.html')
    assert response.status_code == 200

    # we assume user selects logout
    response = client.get('/logout')
    assert response.status_code == 302


def test_delete():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley', 'is_admin': '0'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        response = client.get('/account')
        assert response.status_code == 200
    
    # user confirms account deletion and should be redirected to home
    with client:
        response = client.post('/delete', data={'confirm_delete': True})
        assert response.status_code == 302

def test_my_shoes():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        response = client.get('/account')
        assert response.status_code == 200
    
    # user selects my_shoes history, gets sent to my_shoes.html
    response = client.get('/my_shoes')
    assert response.status_code == 200
        
def test_order_history():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        response = client.get('/account')
        assert response.status_code == 200
    
    # user selects order history, gets sent to order_history.html
    response = client.get('/order_history')
    assert response.status_code == 200
    
def test_start_listing():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        response = client.get('/account')
        assert response.status_code == 200
    
    # user selects make a listing, gets sent to start_listing.html
    response = client.get('/start_listing')
    assert response.status_code == 200

def test_profile():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        response = client.get('/account')
        assert response.status_code == 200

        # set user_id to 2 for testing purposes
        user_id = 2

        response = client.get(f'/profile/{user_id}')
        if response.status_code == 200: # successful retrieval of profile page
            # load appropriate table for profile page
            user_profile = db.query(UserProfile).filter_by(user_id=user_id).first()
            # do something with user_profile
        elif response.status_code == 404: # user not found
            error_message = "User not found"
            # do something with error_message
        elif response.status_code == 403: # user does not have permission to access profile page
            error_message = "You do not have permission to access this page"
            # do something with error_message

        assert response.status_code in [200, 404, 403] # assert that status code is valid

## Tests to see if the User can get to the Edit Account Details page
## Currently this page does nothing.
def test_edit_account_details_access():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    with client:
        response = client.get('/account')
        assert response.status_code == 200

    response = client.get('/edit_account')
    assert response.status_code == 200
