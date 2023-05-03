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


## Our Database Tables that currently function are User and Payment, so lets test that.

## New user to our database. Redirects to login after registration.
def test_user_registration():
    client = app.test_client()
    response = client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    assert response.status_code == 302

## If User logins correctly, then the user should be redirected to the home page.
def test_user_login():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

## Lets test Payment stuff
## Card details are stored in the Payment table, so we should have a successful page entry.
def test_payment():
    client = app.test_client()
    client.post('register.html', data={'email': 'andertalley@gmail.com', 'password': '1234', 'username': 'andertalley'})
    response = client.post('/login', data={'email': 'andertalley@gmail.com', 'password': '1234'})
    assert response.status_code == 302

    #User has selected a shoe to add to Cart and needs to enter payment details.
    client.post('/process_payment', data={'card_number': '5555123456781234', 'expiration_date': '11/26', 'card_name': 'Ander Talley', 'cvc': '123', 'address': '1234 Your Mom Ln, Starkville, MS'})
    assert response.status_code == 302

def test_shoe():
    # Create a test shoe
    shoe = Shoe(brand='Test Shoe', shoetype='test type', size=11, condition="New", description='This is a test shoe.', price=50, image="test.png", user_id=1)

    # Add the shoe to the database
    db.session.add(shoe)
    db.session.commit()

    # Check that the shoe was added to the database
    assert Shoe.query.filter_by(brand='Test Shoe').first() is not None

    # Delete the shoe from the database
    db.session.delete(shoe)
    db.session.commit()

    # Check that the shoe was deleted from the database
    assert Shoe.query.filter_by(brand='Test Shoe').first() is None
