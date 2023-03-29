# import Flask object from the flask package
from flask import Flask, render_template

# application instance and current Python module
app = Flask(__name__)

"""
app is a decorater that turns the Python functions into Flask view functions
(then converts the function's return values into HTTP responses to be displayed on web)
'/' is referring to a URL for web requests
"""
@app.route('/')

#function
def index():
    return render_template('index.html')