import re
from flask import Flask, session, request, render_template

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Dummy data for products
products = {
    1: {'name': 'Product 1', 'price': 100.99},
    2: {'name': 'Product 2', 'price': 200.99},
    3: {'name': 'Product 3', 'price': 300.99},
    4: {'name': 'Product 4', 'price': 400.99},
    5: {'name': 'Product 5', 'price': 500.99}
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
                    'quantity': quantity,
                    'price': product['price'],
                    'subtotal': quantity * product['price']
                }
                cart_items.append(cart_item)
    return render_template('cart.html', cart_items=cart_items)

# Test functions for pytest

def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_show_product():
    with app.test_client() as client:
        response = client.get('/product/1')
        assert response.status_code == 200

def test_add_to_cart():
    with app.test_client() as client:
        response = client.post('/add_to_cart', data={'product_id': '1', 'quantity': '2'})
        assert response.data == b'Item added to cart'

def test_view_cart():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['cart'] = {1: 2}
        response = client.get('/cart')
        assert response.status_code == 200
        assert b'Product 1' in response.data

if __name__ == '__main__':
    app.run(debug=True)

