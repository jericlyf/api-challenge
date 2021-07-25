import requests
import json
import boto3
import botocore
from datetime import datetime

def lambda_handler(event=None,context=None):
    s3 = boto3.client('s3')
    s3_bucket = 'tdf-gemini-challenge'
    s3_object = 'output'
    s3_filename = get_s3_filename()
    tmp_file = '/tmp/' + s3_filename

    resp = get_gemini_market()
    if type(resp) is int:
        return gemini_error(resp)
    else:
        price = resp
    
    data = {}
    data['timestamp'] = str(datetime.now())
    data['prices'] = price

    create_file = open(tmp_file, 'w+')
    create_file.close()

    load_existing_file_from_s3_to_tmp_file(s3, s3_bucket, s3_object, s3_filename, tmp_file)
    write_data_to_file(data, tmp_file)

    if upload_file_to_s3(s3, tmp_file, s3_bucket, s3_object, s3_filename):
        return publish_success()
    else:
        return publish_failed()
    
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

def get_s3_filename():
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    file_name = str(currentDay)+"-"+str(currentMonth)+"-"+str(currentYear)+".txt"
    return file_name

def load_existing_file_from_s3_to_tmp_file(s3, s3_bucket, s3_object, s3_filename, tmp_file):
    try:
        s3_file = str(s3_object) + "/" + str(s3_filename)
        s3.download_file(s3_bucket, s3_file, tmp_file)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            pass
        else:
            raise

def write_data_to_file(data, file):
    output = open(file, "a+")
    output.write(json.dumps(data))
    output.write('\n')
    output.close()

def upload_file_to_s3(s3, file, s3_bucket, s3_object, s3_filename):
    try:
        s3_file = str(s3_object) + "/" + str(s3_filename)
        s3.upload_file(file, s3_bucket, s3_file)
        return True
    except boto3.exceptions.S3UploadFailedError as e:
        if e:
            return False

def publish_success():
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(
        {
        "status": "OK",
        "message": "Prices published to s3"
        }
    )
    return response

def publish_failed():
    response = {}
    response['statusCode'] = 400
    response['body'] = json.dumps(
        {
        "status": "Error",
        "message": "Failed to publish data to s3"
        }
    )
    return response
