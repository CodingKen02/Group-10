import re
from flask import Flask, session, request, render_template
import sys
sys.path.append("source")
from source.app import app
from source.models import *


# Additional flask arguments from Flask database create unique product credentials.
app = Flask(__name__)
# APP IS ACTIVE


def test_index():
    # Define a route for the index page
    response = app.test_client().get('/')

    assert response.status_code == 200


def test_run_app():
    # Help runs the program in web browser
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_go_to_login():
    response = app.test_client().get('/login')
    assert response.status_code == 200

