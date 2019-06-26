import os, sys
import time
import pymongo
from os.path import expanduser
from os.path import join
from bson.json_util import dumps

def database_backup(ip, port, dbName, outputs_dir):
    try:
        print "mongo database Backup downloading......"
        client = pymongo.MongoClient(host=ip, port=port)
        database = client[dbName]
        collections = database.collection_names()
        for i, collection_name in enumerate(collections):
            col = getattr(database,collections[i])
            collection = col.find()
            jsonpath = collection_name + ".json"
            jsonpath = join(outputs_dir, jsonpath)
            with open(jsonpath, 'wb') as jsonfile:
                jsonfile.write(dumps(collection))
        print "backup completed.... storage location :: %s"%(outputs_dir)
    except Exception as er:
        print "Exception Error as %s"%er
    
if __name__ == "__main__":

    mongoIp = sys.argv[1]
    mongoPort = 37017
    dbName = sys.argv[2]

    home = expanduser('~')
    path = home + '/%s/%s'%(mongoIp, dbName)
    print "mongodb backup storing location:: %s"%(path)
    
    if not os.path.exists(path):
        os.makedirs(path)
    outputs_dir = path; 
    database_backup(mongoIp, mongoPort, dbName, outputs_dir)
    


        
