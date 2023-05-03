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

@pytest.mark.parametrize("brand, expected_result", [
    ("Nike", [b'Nike']),
    ("ad", [b'Adidas']),
    ("Gigabyte", [b'No matching items found.']),
    ("Jordans", [b'No matching items found.']),
    ("", [b'Nike', b'Adidas'])
])
def test_search(client, brand, expected_result):
    client = app.test_client()
    response = client.get(f'/search?brand={brand}')
    assert response.status_code == 200
    for result in expected_result:
        assert result in response.data

