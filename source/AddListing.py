from flask import Flask, render_template, request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
