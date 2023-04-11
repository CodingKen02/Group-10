# Create a session object
session = Session()

# Create some example users
user1 = User(name='John', email='john@example.com', password='password1')
user2 = User(name='Jane', email='jane@example.com', password='password2')
user3 = User(name='Bob', email='bob@example.com', password='password3')
session.add_all([user1, user2, user3])
session.commit()

# Create some example shoes
shoe1 = Shoe(name='Air Max 90', brand='Nike', price=120.00, user_id=1)
shoe2 = Shoe(name='Yeezy Boost 350 V2', brand='Adidas', price=220.00, user_id=2)
shoe3 = Shoe(name='Retro 1 High OG', brand='Jordan', price=150.00, user_id=3)
shoe4 = Shoe(name='Chuck Taylor All Star', brand='Converse', price=50.00, user_id=1)
shoe5 = Shoe(name='Classic Slip-On', brand='Vans', price=60.00, user_id=2)
shoe6 = Shoe(name='Superstar', brand='Adidas', price=80.00, user_id=3)
session.add_all([shoe1, shoe2, shoe3, shoe4, shoe5, shoe6])
session.commit()

# Close the session
session.close()
