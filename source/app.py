import re
from flask import Flask, session, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, LoginManager, UserMixin, login_required, logout_user
from models import db, login_manager, User

app = Flask(__name__)
app.secret_key = 'your-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.before_first_request
def create_all():
    db.create_all()

products = {
    1: {'name': 'Air Max 90', 'brand': 'Nike', 'price': 120.00},
    2: {'name': 'Yeezy Boost 350 V2', 'brand': 'Adidas', 'price': 220.00},
    3: {'name': 'Retro 1 High OG', 'brand': 'Jordan', 'price': 150.00},
    4: {'name': 'Chuck Taylor All Star', 'brand': 'Converse', 'price': 50.00},
    5: {'name': 'Classic Slip-On', 'brand': 'Vans', 'price': 60.00},
    6: {'name': 'Superstar', 'brand': 'Adidas', 'price': 80.00}
}


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
     
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/')
     
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
 
        if User.query.filter_by(email=email).first():
            return ('Email already Present')
             
        user = User(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/logoutconfirm')
def logoutconfirm():
    return render_template('logout.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/account')
def show_user_account():
    if current_user.is_authenticated:
        return render_template('account.html')
    else:
        return redirect(url_for('login'))

def upload_image_contents(image):
    # Uploads the image to cloud storage and returns the URL
    # Here is an example using Google Cloud Storage and the google-cloud-storage library
    # We can always change this; it was easy to install though
    from google.cloud import storage
    client = storage.Client()
    bucket_name = 'my-bucket'
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(image.filename)
    blob.upload_from_file(image)
    return f"https://storage.googleapis.com/{bucket_name}/{blob.name}"

def save_listing_to_database(title, description, price, image_urls):
    # Saves the listing to the database
    # Here is an example using SQLAlchemy and a Listing model
    from flask_sqlalchemy import SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listings.db'
    db = SQLAlchemy(app)
    class Listing(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80), nullable=False)
        description = db.Column(db.String(500), nullable=False)
        price = db.Column(db.Float, nullable=False)
        image_urls = db.Column(db.String(500), nullable=False)

        def __repr__(self):
            return f'<Listing {self.title}>'

    listing = Listing(title=title, description=description, price=price, image_urls=image_urls)
    db.session.add(listing)
    db.session.commit()

@app.route('/seller/listings/new', methods=['GET', 'POST'])
def new_listing():
    if request.method == 'POST':
        # Processes form data and saves new listings to database.
        # This function creates all the parameter that the seller must enter to create the listing. 
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        images = request.files.getlist('images')
        # Here is where the images are converted to URLS and added to the cloud.
        image_urls = []
        for image in images:
            # Processing of each individual image.
            image_url = upload_image_contents(image)
            image_urls.append(image_url)
        # Here the listing is successfully created. 
        save_listing_to_database(title, description, price, image_urls)
        return redirect('/seller/listings')
    else:
        # This will display the updated listing form on the website.
        return render_template('new_listing.html')


#THE APP IS RUNNING
#Not sure if we need this anymore?
class Account(db.Model): #This creates a local database that will store the new account type in the server.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    account_type = db.Column(db.String(80), nullable=False)

    def __repr__(self): #Parameters define a unique username.
        return '<Account %r>' % self.username

@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/product/<int:product_id>')
def show_product(product_id):
    product = products.get(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])

    if 'cart' not in session:
        session['cart'] = {}

    if product_id in session['cart']:
        session['cart'][product_id] += quantity
    else:
        session['cart'][product_id] = quantity

    return 'Item added to cart'

@app.route('/cart')
def view_cart():
    cart_items = []

    if 'cart' in session:
        for product_id, quantity in session['cart'].items():
            product = products.get(product_id)
            if product:
                cart_item = {
                    'product_id': product_id,
                    'product_name': product['name'],
                    'brand': product['brand'],
                    'quantity': quantity,
                    'price': product['price'],
                    'subtotal': quantity * product['price']
                }
                cart_items.append(cart_item)

    return render_template('cart.html', cart_items=cart_items)

# Define a route for the payment page
@app.route('/payment')
def payment():
    # Render the payment page template
    return render_template('payment.html')

# Define a route for processing payments via a POST request
@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Retrieve the credit card information from the POST request
    card_number = request.form['card_number']
    expiration_date = request.form['expiration_date']
    card_name = request.form['card_name']
    cvc = request.form['cvc']
#//  $ = active shell environment
    # Validate card number
    if not re.match(r'^\d{16}$', card_number): #User is only allowed to enter 16 digits as the card number
        return 'Invalid card number'

    # Validate expiration date. The input will only allow 2 digits (month) separated by a "/" and another 2 digits (year)
    if not re.match(r'^\d{2}/\d{2}$', expiration_date):
        return 'Invalid expiration date'

    # Validate card name
    if not re.match(r'^[A-Za-z ]+$', card_name):
        return 'Invalid card name'

    # Validate CVC code
    if not re.match(r'^\d{3}$', cvc):
        return 'Invalid CVC code'

    #Validate card type. I know the credentials look a bit complicated let me explain LOL. 
    #Pretty much each parameter will validate the card type based on the first 4 digits in Layman's terms. 
    #The only accepted card types are Visa, Discover, AE, and Discover. We should avoid bank routing for the time being. 
    #We want to avoid encryption protocols which would make this get nasty.
    card_type = None
    if re.match(r'^4', card_number):
        card_type = 'Visa'
    elif re.match(r'^5[1-5]', card_number):
        card_type = 'MasterCard'
    elif re.match(r'^3[47]', card_number):
        card_type = 'American Express'
    elif re.match(r'^6(?:011|5)', card_number):
        card_type = 'Discover'

    # If the card type cannot be determined, return an error message
    if card_type is None:
        return 'Invalid card type'

    # Payment processing would go here, however, we will just skip over this. It is not necessary for Sprint 3

    # Return a success message to the user
    return 'Payment processed successfully'


@app.route('/listings')
def listings():
    return render_template('listings.html')

@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/edit_account')
def edit_account():
    return render_template('edit_account.html')

@app.route('/order_history')
def order_history():
    return render_template('order_history.html')

@app.route('/user_items')
def user_items():
    return render_template('user_items.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
