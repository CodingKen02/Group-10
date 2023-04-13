import re
from flask import Flask, session, request, render_template

# Additional flask arguments from Flask database create unique product credentials.
app = Flask(__name__)
# APP IS ACTIVE


def test_index():
    # Define a route for the index page
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b"Welcome to the index page" in response.data


def test_run_app():
    # Help runs the program in web browser
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

