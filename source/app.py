import re
from flask import Flask, session, request, render_template

app = Flask(__name__)
app.secret_key = 'your-secret-key'

products = {
    1: {'name': 'Air Max 90', 'brand': 'Nike', 'price': 120.00},
    2: {'name': 'Yeezy Boost 350 V2', 'brand': 'Adidas', 'price': 220.00},
    3: {'name': 'Retro 1 High OG', 'brand': 'Jordan', 'price': 150.00},
    4: {'name': 'Chuck Taylor All Star', 'brand': 'Converse', 'price': 50.00},
    5: {'name': 'Classic Slip-On', 'brand': 'Vans', 'price': 60.00},
    6: {'name': 'Superstar', 'brand': 'Adidas', 'price': 80.00}
}

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

# Help runs the program in web browser
if __name__ == '__main__':
    app.run(debug=True)

