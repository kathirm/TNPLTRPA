import boto3
import sys, os
from boto.s3.key import Key
import boto


def Download():
	keyId = '',
	skeyId = '',
	srcfile = 'A.John Britto'
	destfilename  = 'A.John Britto'  
	#localpath = '/home/tfs/Desktop/Kathir/AWS/'
	bucketname = 'facerec'

	conn = boto.connect_s3(keyId, skeyId)
	bucket = conn.get_bucket(bucketname)
	k=Key(bucket,srcfile)
	k.get_contents_to_filename(destfilename)
	print ("File Download complete..!!!")
	for file_key in bucket.list():
		print file_key.name


Download()
