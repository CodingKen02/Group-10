##this will be done in Sprint 4

import re
import pytest
from flask import session, request, render_template
from flask_login import login_user, logout_user
import sys
import os
sys.path.append("source")
sys.path.append("source/instance")
from source.models import *
from source.instance import *
from app import app, db, Shoe

from sqlalchemy.engine import Engine
from sqlalchemy import event

# Create a Nike shoe
nike = Shoe(
    brand='Nike',
    name='Air Force 1',
    price=90,
    description='The Nike Air Force 1 is a classic shoe.',
    image_file='air_force_1.jpg'
)

# Create an Adidas shoe
adidas = Shoe(
    brand='Adidas',
    name='Superstar',
    price=80,
    description='The Adidas Superstar is a classic shoe.',
    image_file='superstar.jpg'
)

@pytest.mark.parametrize("brand, expected_result", [
    ("Nike", [b'Nike']),
    ("ad", [b'Adidas']),
    ("Gigabyte", [b'No matching items found.']),
    ("Jordans", [b'No matching items found.']),
    ("", [b'Nike', b'Adidas'])
])
def test_search(brand, expected_result):
    client = app.test_client()
    with client:  
        response = client.get(f'/search?brand={brand}')
        assert response.status_code == 200
        for result in expected_result:
            assert result in response.data

