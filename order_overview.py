from flask import Flask, render_template
app = Flask(__name__)



@app.route('/order_overview/<username>/<name>/<address>/<city>/<state>/<zip_code>/<card_number>/<card_type>')
def order_overview(username, name, address, city, state, zip_code, card_number, card_type):
    # Get the last 4 digits of the card number
    last_four_digits = card_number[-4:]

    # Render the order overview template with the parameters passed to
    return render_template('order_overview.html', username=username, name=name, address=address, city=city, state=state, zip_code=zip_code, last_four_digits=last_four_digits, card_type=card_type)

    