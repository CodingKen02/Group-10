from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    account_type = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Account %r>' % self.username

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account_type = request.form['account_type']
        new_account = Account(username=username, password=password, account_type=account_type)
        db.session.add(new_account)
        db.session.commit()
        return 'Account created successfully!'
    return render_template('create_account.html')

def test_home():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_create_account():
    with app.test_client() as client:
        response = client.post('/create_account', data=dict(
            username='testuser',
            password='testpassword',
            account_type='Seller'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert b'Account created successfully!' in response.data
