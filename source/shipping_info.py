from flask import Flask, request, render_template
app = Flask(__name__)
@app.route ('/shipping_info', methods=['POST'])
def shipping_info():
    name = request.form['name']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip_code']

    if not name or not address or not city or not state or not zip_code:
        return 'Invalid Shipping information. Please try again'
    else:
        return 'Shipping updated successfully!'
