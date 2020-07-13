import requests
import json

def test_post_headers_body_json():
    url = 'https://amazonsellerproductinfo.herokuapp.com/getproductdetails/scrape?SellerID=A19R3BN6ZSO9A1'
    
    # convert dict to json by json.dumps() for body data. 
    resp = requests.get(url)       
    
    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
