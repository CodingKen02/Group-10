from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import current_user
 
login_manager = LoginManager()
db = SQLAlchemy()
 
class User(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Integer, server_default="0")
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def delete_user(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

    def __repr__(self):
        return f"<User(name='{self.username}', email='{self.email}')>"

class Shoe(db.Model):
    __tablename__ = 'shoes'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    shoetype = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(User, backref='shoes')

    def __repr__(self):
        return f"<Shoe(brand='{self.brand}', shoe='{self.shoetype}', size='{self.size}', condition='{self.condition}', description='{self.description}', price='{self.price}', image='{self.image}', user='{self.user}')>"

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer)
    exp_date = db.Column(db.String(6))
    card_name = db.Column(db.String(80))
    cvc = db.Column(db.Integer)
    address = db.Column(db.String(200))

    def __repr__(self):
        return f"<Card(card_number='{self.card_number}', exp_date='{self.exp_date}', card_name='{self.card_name}', cvc='{self.cvc}', address='{self.address}')>"

 
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))




