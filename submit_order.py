from flask import Flask, render_template, flash, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/submit_order', methods=['POST'])
def submit_order():
    # Flash function will return the message below after the order has been confirmed from the user.
    flash('Thank you! Your order has been confirmed.')

    # Return using the redirect function which branches the function to the HTML file.
    return redirect(url_for('order_confirmation'))

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')
#Render is returned.