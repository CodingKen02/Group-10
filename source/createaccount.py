from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
db = SQLAlchemy(app)
#THE APP IS RUNNING
class Account(db.Model): #This creates a local database that will store the new account type in the server.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    account_type = db.Column(db.String(80), nullable=False)

    def __repr__(self): #Parameters define a unique username.
        return '<Account %r>' % self.username

@app.route('/')
def home(): #Simply a function that creates a route to the homepage. 
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
#This is the create account function that will enable the user to create either a Seller or Consumer account.
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account_type = request.form['account_type']
        new_account = Account(username=username, password=password, account_type=account_type)
        db.session.add(new_account)
        db.session.commit()
        return 'Account created successfully!'
    return render_template('create_account.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)