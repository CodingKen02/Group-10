import re
from flask import Flask, session, request, render_template
import sys
sys.path.append("source")
from source.app import app
from source.models import *


#### These tests test website pathing ####
def test_index():
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_index_another_way():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_go_to_login():
    response = app.test_client().get('/login')
    assert response.status_code == 200

def test_go_to_listings():
    response = app.test_client().get('/listings')
    assert response.status_code == 200

def test_go_to_payment():
    response = app.test_client().get('payment.html')
    assert response.status_code == 200

