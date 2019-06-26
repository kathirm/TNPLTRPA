import os,json, sys
from os.path import expanduser
from pymongo import MongoClient
from bson import json_util

def py_read_folderfiles(dbName):
    try:
        home = expanduser('~')
        path = home + "/157.230.255.60/%s"%dbName
        print "getting file directory ==> %s"%path
        for filename in os.listdir(path):
            locfile = path + "/" + filename
            with open(locfile, "r") as f:
                 for line in f.readlines():
                    datas = json_util.loads(line)
                    jsonName = filename[:-5]
                    client = MongoClient('10.6.7.88',27017)
                    print "connecting mongodb....%s"%client
                    db = client[dbName]
                    collName = db[jsonName]
                    print collName
                    collName.insert(datas)
                    client.close()
    except Exception as er:
        print "Exception error %s"%er


if __name__ == "__main__":

    dbName = sys.argv[1]; 
    py_read_folderfiles(dbName)
