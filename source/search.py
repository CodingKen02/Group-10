#This is just for the testsearch file.

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

@app.route('/search')
def search():
    brand = request.args.get('brand')

    shoes = Shoe.query.filter(
        Shoe.brand.ilike(f'%{brand}%'),
    ).all()

    return render_template('search.html', shoes=shoes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
