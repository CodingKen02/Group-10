from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '123'

# This route displays the login form
@app.route('/login', methods=['GET'])
def userlogin():
    return render_template('userlogin.html')

# This route handles the login form submission
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    # Check if the username and password are valid
    # Replace this with your own authentication logic
    if username == 'example' and password == 'password':
        session['username'] = username
        return redirect(url_for('home'))
    else:
        error = 'Invalid username or password. Please try again.'
        return render_template('login.html', error=error)

# This route logs the user out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# This route displays the home page
@app.route('/')
def home():
    # Check if the user is logged in
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
