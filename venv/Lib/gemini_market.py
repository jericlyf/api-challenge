import requests
import json

def lambda_handler(event=None,context=None):
    resp = get_gemini_market()
    if type(resp) is int:
        return gemini_error(resp)
    else:
        price = resp

    # publish_to_s3()
    # return response

def get_gemini_market():
    base_url = "https://api.gemini.com/v1"
    response = requests.get(base_url + "/pricefeed")
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code()

def gemini_error(statusCode):
    response = {}
    response.statusCode = statusCode
    response.body = json.dumps(
        {
        "status": "Error",
        "message": "Failed to publish data to s3 with statusCode: " + str(statusCode)
        }
    )
    return response
