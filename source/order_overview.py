from flask import Flask, render_template, request, redirect 
app = Flask(__name__)


# Define global variables to store the shipping information
shipping_info = {}

@app.route('/shipping_info', methods=['POST'])
def save_shipping_info():
    global shipping_info
    shipping_info['address'] = request.form['address']
    shipping_info['city'] = request.form['city']
    shipping_info['state'] = request.form['state']
    shipping_info['zip_code'] = request.form['zip_code']
    return redirect('/order_overview')

@app.route('/order_overview')
def order_overview():
    global shipping_info
    return render_template('order_overview.html', name=shipping_info.get('name'), address=shipping_info.get('address'), city=shipping_info.get('city'), state=shipping_info.get('state'), zip_code=shipping_info.get('zip_code'))

if __name__ == '__main__':
    app.run(debug=True)


    