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

def test_search():
    client = app.test_client()
    with client:  
        response = client.get('/search?brand=Nike')
        assert response.status_code == 200
        assert b'Nike' in response.data
        assert b'Adidas' not in response.data

