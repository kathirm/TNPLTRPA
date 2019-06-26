import json, os, sys
import boto3
from boto3.session import Session
import boto

def s3_conn():
    try:
        dev1 = {
                "s3Url"       : "https://s3.pilot.wasabibeta.com",
                "s3SecretKey" : "OUmHWz04XMCjbXAtnKBuWvNz9LBi60bYfdOV442o", 
                "s3AccessKey" : "FM4863R8ZSIODSBVQ4P6", 
                "region_name" : "us-east-1"
               }
        conn = boto3.client('s3', 
                endpoint_url = dev1.get("s3Url"), 
                aws_access_key_id = dev1.get("s3AccessKey"), 
                aws_secret_access_key = dev1.get("s3SecretKey"),
                region_name = dev1.get("region_name")
                )
        print "s3 connection done :: %s"%conn
        get_s3_buckets(conn)
        download_files(conn)
    except Exception as er:
        print "wasabi s3_connection error :: %s"%er
    return conn

def get_s3_buckets(conn):
    try:
        buckets = [] 
        resp = conn.list_buckets()
        buckets = [bucket['Name'] for bucket in resp['Buckets']]
        print "s3 contains list of buckets :: %s"%buckets
    except Exception as er:
        print "get s3 bucketsName Exception error :: %s"%er

    return buckets

def download_files(conn):
    try:
        file_name = "M Eswari/M Eswari_1.jpg"
        bucket_name = "facerec"
        temp_dir = "/home/kathir/M Eswari/M Eswari_1.jpg"


        down_load = conn.download_file(bucket_name, file_name, temp_dir)
        print down_load
    except Exception as er:
        print "download_function exception error :: %s"%er


if __name__ == "__main__":
    s3_conn()
