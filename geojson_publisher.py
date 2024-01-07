"""
geojson_publisher.py
Uploads a geojson file to Mapbox via APIs
"""
import os
import pandas as pd
from pathlib import Path
import json
import helpers as hp
import requests
from dotenv import load_dotenv, set_key
from os.path import join, dirname
import boto3
from datetime import datetime, timedelta
from requests.exceptions import RequestException

dotenv_path = join(dirname(__file__), "frontend/use-mapbox-gl-js-with-react/",'.env')
load_dotenv(dotenv_path)

def renew_creds():
    """
    check in .env to see if credentials are more than 30 minutes old
    :return: bool if creds are expired
    """
    set_time = os.getenv("CRED_TIMESTAMP")  # time that AWS credentials were recently updated in .env
    expiration = timedelta(minutes=30)
    if datetime.now() - datetime.strptime(set_time, "%Y-%m-%d %H:%M:%S.%f") > expiration:
        print("Credentials are expired")
        return True
    else:
        print("Credentials are fresh")
        return False

def update_keys(creds):
    """
    Overwrite the AWS credentials in .env with new creds
    :param creds: dictionary of creds
    :return: None
    """
    print("Overwriting keys")
    set_key(dotenv_path, "BUCKET", creds["bucket"])
    set_key(dotenv_path, "KEY", creds["key"])
    set_key(dotenv_path, "ACCESSKEYID", creds["accessKeyId"])
    set_key(dotenv_path, "SECRETACCESSKEY", creds["secretAccessKey"])
    set_key(dotenv_path, "SESSIONTOKEN", creds["sessionToken"])
    set_key(dotenv_path, "CRED_TIMESTAMP",str(datetime.now()))
    print("Keys updated in .env")
    return

def get_aws_creds(overwrite_keys=False):
    """
    Gets temporary AWS creds from Mapbox endpoint
    If our stored credentials are too old and overwrite_keys is True, overwrite them
    overwrite_keys: bool flag to indicate if the .env file is overwritten
    :return: dictionary creds=AWS credentials
    """
    creds = {}
    if not renew_creds():  # Check if credentials are outdated
        creds["bucket"] = os.getenv("BUCKET")
        creds["key"] = os.getenv("KEY")
        creds["accessKeyId"] = os.getenv("ACCESSKEYID")
        creds["secretAccessKey"] = os.getenv("SECRETACCESSKEY")
        creds["sessionToken"] = os.getenv("SESSIONTOKEN")
    else:
        url = "https://api.mapbox.com/uploads/v1/derekjw99/credentials"
        params = {
            'access_token': os.getenv("MAPBOX_SECRET_ACCESS_TOKEN")  # REACT_APP_MAPBOX_ACCESS_TOKEN
        }
        try:
            r = requests.post(url=url, params=params)
            print(r)
            creds = r.json()
            if overwrite_keys:
                update_keys(creds)
        except RequestException as e:
            print("Failed to get new keys:", e)
    return creds

def copy_to_s3(path, file_name, creds):
    """
    Simialar to running "aws s3 cp /path/to/file s3://{bucket}/{key} --region us-east-1"
    Copies a local geojson file to s3 to stage it for a Mapbox tileset upload
    :param path: path to the geojson file
    :param file_name: name of the geojson file
    :param creds: AWS credentials from Mapbox
    :return: None
    """
    path_to_geo = join(path, file_name)
    bucket_name = creds["bucket"]
    key = creds["key"]
    access_Key_Id = creds["accessKeyId"]
    secret_Access_Key = creds["secretAccessKey"]
    aws_session_token = creds["sessionToken"]
    print("Configuring client")
    s3_client = boto3.client('s3', region_name="us-east-1", aws_access_key_id=access_Key_Id, aws_secret_access_key=secret_Access_Key, aws_session_token=aws_session_token)
    print("Uploading file...")
    s3_client.upload_file(Filename=path_to_geo, Bucket=bucket_name, Key=key)
    print("Uploaded")
    return

def publish(creds):
    """
    Uploads a staged geojson file from S3
    :param creds: AWS credentials from Mapbox
    :return: ret_data=requests.post() response
    """
    url = "https://api.mapbox.com/uploads/v1/derekjw99"
    bucket_name = creds["bucket"]
    key_name = creds["key"]
    params = {
        'access_token': os.getenv("MAPBOX_SECRET_ACCESS_TOKEN"),
    }
    ret_data = None
    payload = {
        "url": "https://{bucket}.s3.amazonaws.com/{key}".format(bucket=bucket_name, key=key_name),
        "tileset": "{username}.{tileset_name}".format(username="derekjw99", tileset_name="interconnectionGEOJSON"),
        "name": "Updated_Interconnection"
    }
    header = {
        "Content-Type": "application/json"
    }
    try:
        r = requests.post(url=url, headers=header, params=params, data=json.dumps(payload))
        ret_data = r.json()
    except RequestException as e:
        print("POST failed:", e)
    return ret_data

def main():
    path = "/Users/derekwacks/Documents/Interconnection/code/data"
    file_name = "interconnection2.geojson"
    creds = get_aws_creds(overwrite_keys=False)
    print("Creds:", creds)
    copy_to_s3(path, file_name, creds)
    pub_response = publish(creds)
    print(pub_response)
    return

if __name__ == "__main__":
    main()