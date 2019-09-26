import sys, json, os
import boto3
import datetime
from os.path import expanduser

def create_folder(conn, bucket_name, folder_name, db_name):
    try:
        now = datetime.datetime.now()
        getDate = now.strftime('%d%m%Y')
        print "Create Folder Name :: %s"%getDate
        curDate = str(getDate)
        conn.put_object(Bucket=bucket_name, Key=curDate+"/")
        home = expanduser('~')

        path = home +'/%s/%s'%(folder_name, db_name) 
        conn.put_object(Bucket=bucket_name, Key=curDate+"/"+db_name+"/")
        buckpath = str(curDate+"/"+db_name)
        print "WARNING Waiting for Upload data Connection...."
        for filename in os.listdir(path):
            dirpath = buckpath+'/{}'.format(filename)
            file_path = path +"/" +filename
            conn.upload_file(file_path, bucket_name, dirpath)
            print "INFO Upload into bcktName :: {%s} and Bckt_Path :: {%s} and F-name :: {%s} successfully"%(bucket_name, buckpath, filename)
            #uploadInto_s3(conn, filename, bucket_name, file_name) 

    except Exception as er:
        print "Create subFolder Exception :: %s"%er


def uploadInto_s3(conn, file_name, bucket_name, file_path):
    try:
        getFileName = file_name;
        bucketName = bucket_name;
        filename = file_path 
        #filename = '/home/kathir/10.6.7.28/%s'%(getFileName)

        print "Current Upload Folder_Name :: %s && Bucket_Name :: %s"%(folder_name, bucket_name)
        resp = conn.upload_file(filename, bucketName, getFileName)
        print "Upload Done....."
    except Exception as er:
        print "Folder files Upload into s3 Exception :: %s"%er


if __name__ == "__main__":

    folder_name = sys.argv[1]
    bucket_name = "tenantbackups"
    db_name = sys.argv[2]

    conn = boto3.client('s3',
            endpoint_url = "https://s3.us-west-1.wasabisys.com",
            aws_access_key_id = "LCT98JYU5NJB34CV542Z",
            aws_secret_access_key = "8zmOmB62DA6ZUyDCmJqmGHJV0e1il6sdsNTu11oA",
            region_name = "us-west-1"
            );
    print "INFO {#s3} Connection Status {%s}"%conn
    create_folder(conn, bucket_name, folder_name, db_name)

