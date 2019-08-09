import json, os, sys
import boto3
from boto3.session import Session
import boto

def s3_conn():
    try:
        dev1 = {
                "s3Url"       : "",
                "s3SecretKey" : "",
                "s3AccessKey" : "",
                "region_name" : "",
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
        resource = boto3.resource('s3')
        bucket = resource.Bucket('facerec')
        objList = conn.list_objects(Bucket='facerec')['Contents']
        for obj in objList:
            obj_Key = obj['Key']
            path,_destPath = os.path.split(obj_Key)
            print ("Downloading file :"+ obj_Key);
            conn.download_file('facerec', obj_Key, _destPath)
    except Exception as er:
        print "download_function exception error :: %s"%er


if __name__ == "__main__":
    s3_conn()
