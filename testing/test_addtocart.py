# import re
# from flask import Flask, session, request, render_template

# app = Flask(__name__)
# app.secret_key = 'your-secret-key'

# # Dummy data for products
# products = {
#     1: {'name': 'Air Max 90', 'brand': 'Nike', 'price': 120.00},
#     2: {'name': 'Yeezy Boost 350 V2', 'brand': 'Adidas', 'price': 220.00},
#     3: {'name': 'Retro 1 High OG', 'brand': 'Jordan', 'price': 150.00},
#     4: {'name': 'Chuck Taylor All Star', 'brand': 'Converse', 'price': 50.00},
#     5: {'name': 'Classic Slip-On', 'brand': 'Vans', 'price': 60.00},
#     6: {'name': 'Superstar', 'brand': 'Adidas', 'price': 80.00}
# }

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/product/<int:product_id>')
# def show_product(product_id):
#     product = products.get(product_id)
#     return render_template('product.html', product=product)

# @app.route('/add_to_cart', methods=['POST'])
# def add_to_cart():
#     product_id = int(request.form['product_id'])
#     quantity = int(request.form['quantity'])
#     if 'cart' not in session:
#         session['cart'] = {}
#     if product_id in session['cart']:
#         session['cart'][product_id] += quantity
#     else:
#         session['cart'][product_id] = quantity
#     return 'Item added to cart'

# @app.route('/cart')
# def view_cart():
#     cart_items = []
#     if 'cart' in session:
#         for product_id, quantity in session['cart'].items():
#             product = products.get(product_id)
#             if product:
#                 cart_item = {
#                     'product_id': product_id,
#                     'product_name': product['name'],
#                     'brand': product['brand'],
#                     'quantity': quantity,
#                     'price': product['price'],
#                     'subtotal': quantity * product['price']
#                 }
#                 cart_items.append(cart_item)
#     return render_template('cart.html', cart_items=cart_items)

# # Test functions for pytest

# def test_index():
#     with app.test_client() as client:
#         response = client.get('/')
#         assert response.status_code == 200

# def test_show_product():
#     with app.test_client() as client:
#         response = client.get('/product/1')
#         assert response.status_code == 200

# def test_add_to_cart():
#     with app.test_client() as client:
#         response = client.post('/add_to_cart', data={'product_id': '1', 'quantity': '1'})
#         assert response.data == b'Item added to cart'

# def test_view_cart():
#     with app.test_client() as client:
#         with client.session_transaction() as session:
#             session['cart'] = {1: 1}
#         response = client.get('/cart')
#         assert response.status_code == 200
#         assert b'Air Max 90' in response.data
#         assert b'Nike' in response.data
#         assert b'120.0' in response.data

# if __name__ == '__main__':
#     app.run(debug=True)
