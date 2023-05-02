import sqlite3

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
              password_hash TEXT)''')

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

conn.commit()
conn.close()
