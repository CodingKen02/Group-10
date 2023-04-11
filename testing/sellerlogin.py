from flask import Flask, request, session, redirect, url_for

app = Flask(__name__)

# SECURITY (SECRET KEY)
app.secret_key = '123'

# Routing for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Username and password are required for access to account.
        username = request.form['username']
        password = request.form['password']

        # The username and passwords must be correct otherwise access will be denied.
        if username == 'seller' and password == 'password':
            # If the username and password are valid, create a session for the seller.
            session['seller'] = True
            return redirect(url_for('dashboard'))
        else:
            # if the username and password are invalid, display error message. They must try again.
            return 'Invalid login credentials. Please try again.'

    # If GET then the algorithm will return. 
    return '''
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br>

            <input type="submit" value="Log In">
        </form>
    '''

# Dashboard route (Seller must be logged in)
@app.route('/dashboard')
def dashboard():
    # This function will lead to the dashboard being displayed. 
    if 'seller' not in session:
        # If the seller is not logged in, redirect to the login page.
        return redirect(url_for('login'))

    # If the seller is logged in, then this message will be displayed.
    return 'Welcome to the seller dashboard!'

# Logout route
@app.route('/logout')
def logout():
    # End seller session.
    session.pop('seller', None)

    # Redirect to the login page.
    return redirect(url_for('login'))
