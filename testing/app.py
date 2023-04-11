import re # Importing re package will provide additional arguments from the flask database.
from flask import Flask, session, request, render_template
# Additional flask arguments from Flask database create unique product credentials.
app = Flask(__name__)
# APP IS ACTIVE
app.secret_key = 'your-secret-key'

# Dummy data for products
products = {
    1: {'name': 'Product 1', 'price': 100.99},
    2: {'name': 'Product 2', 'price': 200.99},
    3: {'name': 'Product 3', 'price': 300.99},
    4: {'name': 'Product 4', 'price': 400.99},
    5: {'name': 'Product 5', 'price': 500.99}
}
# Define a route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for the product page that takes a product ID as a parameter
@app.route('/product/<int:product_id>')
def show_product(product_id):
    # Retrieve product information from database
    # Product ID can be generated at random. That is optional. 
    product = products.get(product_id)

    # Render the product page template with the retrieved product information
    return render_template('product.html', product=product)

# Define a route for adding items to the cart via a POST request
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Retrieve the product ID and quantity from the POST request
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])

    # Product ID generated. The quantity will vary based on product. Would be easier to maintain the same quantity in the database. 
    # Check if the cart exists in the session
    if 'cart' not in session:
        session['cart'] = {}

    # Add the product and quantity to the cart in the session
    if product_id in session['cart']:
        session['cart'][product_id] += quantity
    else:
        session['cart'][product_id] = quantity

    # Return a success message
    return 'Item added to cart'

# Define a route for the cart page
@app.route('/cart')
def view_cart():
    cart_items = []

    # Check if the cart exists in the session
    if 'cart' in session:
        # This function assigns the product ID, product name, quantity, price, and subtotal which to the view_cart function or "order".
        # ...
        # Iterate over the cart items in the session
        for product_id, quantity in session['cart'].items():
            # Retrieve the product information from the database
            product = products.get(product_id)
            if product:
                # Create a cart item dictionary with the retrieved product information
                cart_item = {
                    'product_id': product_id,
                    'product_name': product['name'],
                    'quantity': quantity,
                    'price': product['price'],
                    'subtotal': quantity * product['price']
                }
                # Add the cart item to the list of cart items
                cart_items.append(cart_item)
    # Render the cart page template with the list of cart items
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

