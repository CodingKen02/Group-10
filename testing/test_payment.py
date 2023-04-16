# import re
# from flask import Flask, request, render_template

# app = Flask(__name__)

# @app.route('/')
# def payment():
#     return render_template('payment.html')

# @app.route('/payment', methods=['POST'])
# def process_payment(card_number, expiration_date, card_name, cvc):

#     #These are the .html requests
#     #card_number = request.form['card_number']
#     #expiration_date = request.form['expiration_date']
#     #card_name = request.form['card_name']
#     #cvc = request.form['cvc']

#     # Validate card number
#     if not re.match(r'^\d{16}$', card_number):
#         return 'Invalid card number'

#     # Validate expiration date
#     if not re.match(r'^\d{2}/\d{2}$', expiration_date):
#         return 'Invalid expiration date'

#     # Validate card name
#     if not re.match(r'^[A-Za-z ]+$', card_name):
#         return 'Invalid card name'

#     # Validate CVC code
#     if not re.match(r'^\d{3}$', cvc):
#         return 'Invalid CVC code'

#     # Validate card type
#     card_type = None
#     if re.match(r'^4', card_number):
#         card_type = 'Visa'
#     elif re.match(r'^5[1-5]', card_number):
#         card_type = 'MasterCard'
#     elif re.match(r'^3[47]', card_number):
#         card_type = 'American Express'
#     elif re.match(r'^6(?:011|5)', card_number):
#         card_type = 'Discover'

#     #if card_type is None:
#     #    return 'Invalid card type'

#     return 'Payment processed successfully'

# # Test Functions

# def test_invalid_card_number():
#     assert process_payment('1234', '01/25', 'John Doe', '123') == 'Invalid card number'

# def test_invalid_expiration_date():
#     assert process_payment('1234567890123456', '01/01/2', 'John Doe', '123') == 'Invalid expiration date'

# def test_invalid_card_name():
#     assert process_payment('1234567890123456', '01/25', '1', '123') == 'Invalid card name'

# def test_invalid_cvc():
#     assert process_payment('1234567890123456', '01/25', 'John Doe', '12') == 'Invalid CVC code'

# def test_valid_card_details():
#     assert process_payment('1234567890123456', '01/25', 'John Doe', '123') == 'Payment processed successfully'


