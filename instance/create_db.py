import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('shoe.db')
c = conn.cursor()

# Create a table for shoes
c.execute('''CREATE TABLE IF NOT EXISTS shoes
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              brand TEXT,
              shoetype TEXT,
              size INTEGER,
              condition TEXT,
              description TEXT,
              price INTEGER,
              image TEXT,
              user_id INTEGER,
              FOREIGN KEY (user_id) REFERENCES users(id))''')

# Create a table for users
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              email TEXT UNIQUE,
              username TEXT UNIQUE,
              password_hash TEXT,
              is_admin INTEGER DEFAULT 0)''')

# Create a table for payment
c.execute('''CREATE TABLE IF NOT EXISTS payment_cards
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              card_name TEXT,
              card_number INTEGER,
              exp_date TEXT,
              cvc INTEGER,
              address TEXT,
              user_id INTEGER,
              FOREIGN KEY (user_id) REFERENCES users(id))''')

# Create an initial admin user
admin_password = "password"
admin_password_hash = generate_password_hash(admin_password)
c.execute('''INSERT INTO users (email, username, password_hash, is_admin)
             VALUES (?, ?, ?, ?)''', ("an@admin.com", "an", admin_password_hash, 1))

conn.commit()
conn.close()

