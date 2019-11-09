import json, os 
from boto3.session import Session
import boto3, botocore

ACCESS_KEY = 'U7CIDT7JL83MG217M1AV'
SECRET_KEY = 'wbjdnDUepeT7YhDRNPzkq5fqQyktDWrMsrA4L56K'

conn = boto3.client('s3',
        endpoint_url = "https://s3.wasabibeta.com",
        aws_access_key_id = ACCESS_KEY,
        aws_secret_access_key = SECRET_KEY, 
        region_name = "us-east-1"
        );

response = conn.list_buckets()
buckets = [bucket['Name'] for bucket in response['Buckets']]
print buckets

try:
    conn.download_file('teraface','users.pickle1','/tmp/users.pickle_test')
    print "object download complete....!!!"
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
