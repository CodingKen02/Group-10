##this will be done in Sprint 4

import pytest
from app import app, db, Shoe

@pytest.fixture(scope='module')
def test_client():
    # Set up test client and application context
    with app.test_client() as client:
        with app.app_context():
            # Create test database
            db.create_all()

            # Create test shoes
            nike = Shoe(
                brand='Nike',
                shoetype='Air Force 1',
                size=12,
                condition="New",
                description='The Nike Air Force 1 is a classic shoe.',
                price=90,
                image='air_force_1.jpg',
                user_id=1
            )
            adidas = Shoe(
                brand='Adidas',
                shoetype='Superstar',
                size=12,
                condition="New",
                description='The Adidas Superstar is a classic shoe.',
                price=80,
                image='superstar.jpg',
                user_id=1
            )

            # Add shoes to database
            db.session.add(nike)
            db.session.add(adidas)
            db.session.commit()

            yield client

            # Remove test data
            db.session.delete(nike)
            db.session.delete(adidas)
            db.session.commit()
            db.drop_all()

@pytest.mark.parametrize("brand, expected_result", [
    ("Nike", [b'Nike']),
    ("ad", [b'Adidas']),
    ("Gigabyte", [b'No matching items found.']),
    ("Jordans", [b'No matching items found.']),
    ("", [b'Nike', b'Adidas'])
])
def test_search(test_client, brand, expected_result):
    response = test_client.get(f'/search?brand={brand}')
    assert response.status_code == 200
    for result in expected_result:
        assert result in response.data


