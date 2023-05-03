##this will be done in Sprint 4

import re
from flask import Flask, session, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, LoginManager, UserMixin, login_required, logout_user
from models import db, login_manager, User, Shoe, Payment
import os

app = Flask(__name__, static_folder='static')

app.secret_key = 'your-secret-key'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

def test_search(client):
    # Test case 1: Search by keyword
    response = client.get('/search?brand=Nike')
    assert response.status_code == 200
    assert b'Nike' in response.data
    assert b'Adidas' not in response.data

    # Test case 2: Search by character(s)
    response = client.get('/search?brand=ad')
    assert response.status_code == 200
    assert b'Adidas' in response.data
    assert b'Nike' not in response.data

    # Test case 3: Search non-existing shoe brand
    response = client.get('/search?brand=Gigabyte')
    assert response.status_code == 200
    assert b'No matching items found.' in response.data

    # Test case 4: Search shoe type in search bar
    response = client.get('/search?brand=Jordans')
    assert response.status_code == 200
    assert b'No matching items found.' in response.data

    # Test case 5: Press search button for all shoes
    response = client.get('/search')
    assert response.status_code == 200
    assert b'Nike' in response.data
    assert b'Adidas' in response.data
    assert b'Jordan' in response.data
