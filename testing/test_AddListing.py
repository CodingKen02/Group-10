# from flask import Flask, render_template, request
# import pytest

# app = Flask(__name__)

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# def test_new_listing_form(client):
#     response = client.get('/seller/listings/new')
#     assert response.status_code == 200
#     assert b"New Listing Form" in response.data

# def test_new_listing_submission(client, monkeypatch):
#     # Mock the upload_image_contents and save_listing_to_database functions
#     def mock_upload_image_contents(image):
#         return 'https://www.example.com/image.jpg'

#     def mock_save_listing_to_database(title, description, price, image_urls):
#         pass

#     monkeypatch.setattr('module.upload_image_contents', mock_upload_image_contents)
#     monkeypatch.setattr('module.save_listing_to_database', mock_save_listing_to_database)

#     # Create a sample form submission data
#     form_data = {
#         'title': 'Test Listing',
#         'description': 'This is a test listing',
#         'price': '100.00',
#         'images': [
#             (BytesIO(b'test image data'), 'test.jpg'),
#             (BytesIO(b'another test image data'), 'test2.jpg')
#         ]
#     }

#     # Make a POST request to submit the form data
#     response = client.post('/seller/listings/new', data=form_data, content_type='multipart/form-data')

#     # Assert that the submission was successful and the user was redirected to the correct page
#     assert response.status_code == 302
#     assert response.location == 'http://localhost/seller/listings'

# def test_new_listing_submission_invalid_data(client):
#     # Create a sample form submission data with invalid price
#     form_data = {
#         'title': 'Test Listing',
#         'description': 'This is a test listing',
#         'price': 'abc',
#         'images': [
#             (BytesIO(b'test image data'), 'test.jpg'),
#             (BytesIO(b'another test image data'), 'test2.jpg')
#         ]
#     }

#     # Make a POST request to submit the form data
#     response = client.post('/seller/listings/new', data=form_data, content_type='multipart/form-data')

#     # Assert that the submission failed and the form was displayed again with an error message
#     assert response.status_code == 200
#     assert b"Invalid price" in response.data
#     assert b"New Listing Form" in response.data

