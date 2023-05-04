import re
from flask import Flask, session, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, LoginManager, UserMixin, login_required, logout_user
from .models import db, login_manager, User, Shoe, Payment
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

@app.route('/return_order', methods=['POST'])
def return_order():
    return_number = request.form['return_number']
    reason = request.form['reason']
    # You can implement your return order logic here, such as saving the return request to a database
    return render_template('return_success.html')

@app.route('/search')
def search():
    brand = request.args.get('brand')

    shoes = Shoe.query.filter(
        Shoe.brand.ilike(f'%{brand}%'),
    ).all()

    return render_template('search.html', shoes=shoes)

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

@app.route('/listings2', methods=['GET', 'POST'])  # NEW FUNCTION THAT WORKS FOR LISTING A SHOE -kk
def listings2():
    if request.method == 'POST':
        brand = request.form['brand']
        shoetype = request.form['shoetype']
        size = request.form['size']
        condition = request.form['condition']
        description = request.form['description']
        price = request.form['price']
        image = request.files['image']

        filename = image.filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        shoe = Shoe(
            brand=brand,
            shoetype=shoetype,
            size=size,
            condition=condition,
            description=description,
            price=price,
            image=filename
        )

        db.session.add(shoe)
        db.session.commit()

    shoes = Shoe.query.all()
    return render_template('listings2.html', shoes=shoes)

@app.route('/start_listing') # NEW FUNCTION THAT WORKS FOR LISTING A SHOE -kk
def start_listing():
    return render_template('start_listing.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
     
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email = email).first()
        print(email)
        if user is not None and user.check_password(request.form['password']):
            login_user(user)         
            return redirect('/')
     
    return render_template('login.html')

@app.route('/register.html', methods=['POST', 'GET'])
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

@app.route('/logout.html')
def logout2():
        logout_user()
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

def save_listing_to_database(title, brand, description, price, image_urls): # NOT USING THIS

    userid = current_user.id
    user = current_user
    listing = Shoe(name=title, brand=brand, description=description, price=price, image_urls=image_urls, userid=userid, user=user)
    db.session.add(listing)
    db.session.commit()
    return True

@app.route('/seller/listings/new', methods=['GET', 'POST']) # NOT USING THIS
def new_listing():
    if request.method == 'POST':
        # Processes form data and saves new listings to database.
        # This function creates all the parameter that the seller must enter to create the listing. 
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        images = request.files.getlist('images')
        brand = request.form['brand']
        # Here is where the images are converted to URLS and added to the cloud.
        image_urls = []
        # for image in images:
            # Processing of each individual image.
            # image_url = upload_image_contents(image)
            # image_urls.append(image_url)
        # Here the listing is successfully created. 
        if (save_listing_to_database(title, brand, description, price, image_urls)):
            return redirect('/seller/listings')
    
    else:
        # This will display the updated listing form on the website.
        return render_template('new_listing.html')


#THE APP IS RUNNING
@app.route('/') # UPDATED FUNCTION THAT WORKS FOR LISTING A SHOE -kk
def index():
    image_url = url_for('static', filename='images/AD.png')
    shoes = Shoe.query.all()
    shoe_info = [{'id': shoe.id, 'brand': shoe.brand, 'shoetype': shoe.shoetype, 'size': shoe.size, 'condition': shoe.condition,
                  'description': shoe.description, 'price': shoe.price, 'image': shoe.image} for shoe in shoes]
    return render_template('index.html', shoes=shoe_info, image_url=image_url)

@app.route('/product/<int:product_id>') # NOT USING THIS
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
@app.route('/payment.html')
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
    address = request.form['shipping_info']
#//  $ = active shell environment
    # Validate card number
    if not re.match(r'^\d{16}$', card_number): #User is only allowed to enter 16 digits as the card number
        return 'Order Confirmed. Thank you for your purchase!'

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

    id = current_user.id
    card = Payment(id = id, card_number = card_number, exp_date = expiration_date, card_name = card_name, cvc = cvc, address = address)
    db.session.add(card)
    db.session.commit()
    # Payment processing would go here, however, we will just skip over this. It is not necessary for Sprint 3

    # Return a success message to the user
    return render_template('process_payment.html')


shipping_info = {}

@app.route('/shipping_info', methods=['POST'])
def save_shipping_info():
    global shipping_info
    shipping_info['address'] = request.form['address']
    shipping_info['city'] = request.form['city']
    shipping_info['state'] = request.form['state']
    shipping_info['zip_code'] = request.form['zip_code']
    return redirect('/order_overview')

@app.route('/order_overview', methods=['GET', 'POST'])
def order_overview():
    if request.method == 'POST':
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        expiration_date = request.form['expiration_date']
        card_number = request.form['card_number'][-4:]  # only keep the last 4 digits
        return render_template('order_overview.html', address=address,
                               city=city, state=state, zip_code=zip_code, expiration_date=expiration_date, 
                               last_four_digits=card_number)
    else:
        return redirect(url_for('index'))



@app.route('/listings') # NOT USING THIS
def listings():
    return render_template('listings.html')

@app.route('/delete.html')
def delete2():
        return render_template('delete.html')

@app.route('/delete', methods=['POST'])
def delete():
    # check if the user has confirmed the account deletion
    if 'confirm_delete' not in request.form:
        flash('Please confirm that you want to delete your account.')
        return redirect(url_for('delete_account'))

    # delete the user's account and associated data from the database
    user_id = current_user.id
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    # inform the user that their account has been deleted
    flash('Your account has been successfully deleted.')
    return redirect(url_for('index'))

@app.route('/submit_order.html')
def submit_order():
    return render_template('submit_order.html')

@app.route('/edit_account')
def edit_account():
    return render_template('edit_account.html')

@app.route('/order_history')
def order_history():
    return render_template('order_history.html')

@app.route("/success", methods=["POST"])
def success():
    name = request.form["name"]
    session['name'] = name
    biography = request.form["biography"]
    session['biography'] = biography
    phone = request.form["phone"]
    session['phone'] = phone
    return redirect("/profile")

@app.route("/profile")
def profile():
    name = session.get('name', '')
    biography = session.get('biography', '')
    phone = session.get('phone', '')
    return render_template("profile.html", name=name, biography=biography, phone=phone)

@app.route('/base')
def logo():
    image_url = url_for('static', filename='images/logo.png')
    return render_template('base.html', image_url=image_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
