##this will be done in Sprint 4

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
