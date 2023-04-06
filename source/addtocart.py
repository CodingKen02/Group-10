from flask import Flask, session, request, render_template
#Additional flask arguments from Flask database create unique product credentials.
app = Flask(__name__)
#APP IS ACTIVE
app.secret_key = 'your-secret-key'

@app.route('/product/<int:product_id>')
def show_product(product_id):
    # Retrieve product information from database
    # Product ID can be generated at random. That is optional. 

    return render_template('product.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])

    # Product ID generated. The quantity will vary based on product. Would be easier to maintain the same quantity in the database. 

    if 'cart' not in session: #User cart created. The product ID, cart, and quantity can all be assigned simultaneously. Optional. 
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
        # This function assigns the product ID, product name, quantity, price, and subtotal which to the view_cart function or "order".
        # ...

        for product_id, quantity in session['cart'].items():
            cart_item = {
                'product_id': product_id,
                'product_name': products[product_id]['name'],
                'quantity': quantity,
                'price': products[product_id]['price'],
                'subtotal': quantity * products[product_id]['price']
            }
            cart_items.append(cart_item)

    return render_template('cart.html', cart_items=cart_items)
