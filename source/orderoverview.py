from flask import Flask
app = Flask(__name__)

@app.route('/order_overview', methods=['POST'])
def order_overview():
   #Here we have to retrieve all the information that is being stored and display it to the user.
    #Below is some example data. This information needs to actually be pulled from the Database. 
    user_name = 'apowers123'
    name = "Austin Powers"
    account_ID = 'SNKR1782356'
    shipping_info = '234 CasoPlaza Blvd., 28655, Starkville, MS'
    payment_info = '************5678'
    return render_template('order_overview.html')