<<<<<<< HEAD
from flask import Flask, render_template, request

app = Flask(__name__)

=======
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def upload_image_contents(image):
    # Uploads the image to cloud storage and returns the URL
    # Here is an example using Google Cloud Storage and the google-cloud-storage library
    # Note: we can always change this; it was easy to install though and test in the frontend
    from google.cloud import storage
    client = storage.Client()
    bucket_name = 'my-bucket'
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(image.filename)
    blob.upload_from_file(image)
    return f"https://storage.googleapis.com/{bucket_name}/{blob.name}"

def save_listing_to_database(title, description, price, image_urls):
    # Saves the listing to the database
    # Here is an example using SQLAlchemy and a Listing model
    from flask_sqlalchemy import SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listings.db'
    db = SQLAlchemy(app)
    class Listing(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80), nullable=False)
        description = db.Column(db.String(500), nullable=False)
        price = db.Column(db.Float, nullable=False)
        image_urls = db.Column(db.String(500), nullable=False)

        def __repr__(self):
            return f'<Listing {self.title}>'

    listing = Listing(title=title, description=description, price=price, image_urls=image_urls)
    db.session.add(listing)
    db.session.commit()

>>>>>>> 13f81c179aefa0c7a33a6c93d562e9849219f33f
@app.route('/seller/listings/new', methods=['GET', 'POST'])
def new_listing():
    if request.method == 'POST':
        # Processes form data and saves new listings to database.
        # This function creates all the parameter that the seller must enter to create the listing. 
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        images = request.files.getlist('images')
        # Here is where the images are converted to URLS and added to the cloud.
        image_urls = []
        for image in images:
            # Processing of each individual image.
            image_url = upload_image_contents(image)
            image_urls.append(image_url)
        # Here the listing is successfully created. 
        save_listing_to_database(title, description, price, image_urls)
        return redirect('/seller/listings')
    else:
        # This will display the updated listing form on the website.
        return render_template('new_listing.html')
<<<<<<< HEAD

=======
    
>>>>>>> 13f81c179aefa0c7a33a6c93d562e9849219f33f
if __name__ == '__main__':
    app.run(debug=True)
