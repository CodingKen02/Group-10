import re
from flask import Flask, session, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user, LoginManager, UserMixin

app = Flask(__name__)
app.secret_key = 'your-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)

products = {
    1: {'name': 'Air Max 90', 'brand': 'Nike', 'price': 120.00},
    2: {'name': 'Yeezy Boost 350 V2', 'brand': 'Adidas', 'price': 220.00},
    3: {'name': 'Retro 1 High OG', 'brand': 'Jordan', 'price': 150.00},
    4: {'name': 'Chuck Taylor All Star', 'brand': 'Converse', 'price': 50.00},
    5: {'name': 'Classic Slip-On', 'brand': 'Vans', 'price': 60.00},
    6: {'name': 'Superstar', 'brand': 'Adidas', 'price': 80.00}
}

user_database = {
    1: {'username': 'Ander', 'password': '1234', 'userID': '1'},
    2: {'username': 'Ehren', 'password': '5678', 'userID': '2'}
}

class User(UserMixin):
    user_count = 0

    def __init__(self, username, password, userID=None):
        self.username = username
        self.password = password
        if userID is None:
            User.user_count += 1
            self.userID = User.user_count
        else:
            self.userID = userID

    def get_user(self):
        return self.username

    def get_password(self):
        return self.password

    def get_userid(self):
        return self.userID

    def get_id(self):
        return str(self.userID)

    @classmethod
    def get(cls, username):
        # In a real app, this would fetch the user's information from a database.
        # For simplicity, we'll just hardcode a single user here.
        user_data = get_user_from_db(username)
        if user_data is not None:
            return cls(username=user_data['username'], password=user_data['password'], userID=user_data['userID'])
        return None

def initialize_users():
    users = {}
    for user_id, user_data in user_database.items():
        user = User(username=user_data['username'], password=user_data['password'], userID=user_data['userID'])
        users[user_id] = user
    return users
    
users = initialize_users()

def get_user_from_db(user_id):
    user = user_database.get(user_id)
    if user:
        return User(user['username'], user['password'], user_id)
    else:
        return None

@login_manager.user_loader
def load_user(username):
    # Load the user from your database
    user_data = get_user_from_db(username)

    # If the user exists in the database, create and return a User object
    if user_data:
        return User(username=user_data['username'], password=user_data['password'])

    # If the user does not exist in the database, return None
    return None

@login_manager.request_loader
def load_user_from_request(request):
    # Check if the request is for an anonymous user
    if request.args.get('anonymous'):
        return User(username='anonymous', password=None)

    # Get the user's login credentials from the request
    username = request.form.get('username')
    password = request.form.get('password')

    # If the username or password is missing, return None
    if not username or not password:
        return None

    # Load the user from your database
    user_data = get_user_from_db(username)

    # If the user exists in the database and the password is correct, create and return a User object
    if user_data and password == user_data['password']:
        return User(username=user_data['username'], password=user_data['password'])

    # If the user does not exist in the database or the password is incorrect, return None
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user_id, user_data in user_database.items():
            if username == user_data['username'] and password == user_data['password']:
                user = User(username=user_data['username'], password=user_data['password'], userID=user_data['userID'])
                login_user(user)
                return redirect(url_for('show_user_account'))
        return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html', error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.get(username)
        if user:
            flash('Username already taken')
        else:
            new_user = User(username=username, password=password)
            flash('Registration successful')
            return redirect(url_for('login'))

    return render_template('register.html')

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
def index():
    return render_template('index.html')

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

    #Validate card type. I know the credentials look a bit complicated let me explain. 
    #Pretty much each parameter will validate the card type based on the first 4 digits in Layman's terms. 
    #The only accepted card types are Visa, Discover, AE, and Discover. We should avoid bank routing for the time being. 
    #We want to avoid encryption protocols which would make this unnecsarily complicated.
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

@app.route('/logout')
def logout():
    return render_template('logout.html')

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

@app.route('/order_overview')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
