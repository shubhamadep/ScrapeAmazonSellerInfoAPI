import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

import requests


def test_reviews_route():

    app.testing = True
    with app.test_client(app) as c:

        url = 'http://127.0.0.1:5000/reviews/scrape?ASIN=B07PDXKSGJ'

        resp = c.get(url)

        # Validate status code.
        assert resp.status_code == 200

        # Validate the response is application/json, the error responses are in HTML.
        assert resp.content_type == 'application/json'
