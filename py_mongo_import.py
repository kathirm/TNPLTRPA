import os,json, sys
from os.path import expanduser
from pymongo import MongoClient
from bson import json_util


def py_read_folderfiles(dbInit, dbName, path):
    try:
        exclude = ['Jobs.json', 'Logs.json']; #skip upload datas in mongoDb list append++
        for filename in os.listdir(path):
            if filename not in exclude: 
                jsonName = filename[:-5]
                syspath = path + "/" + filename
                py_upload_collection(dbInit, jsonName, syspath)
    except Exception as er:
        print "Exception Error read_folderFiles func ===> %s"%er

def py_upload_collection(dbInit, collectionName, filePath):
    try:
        collName = dbInit[collectionName]
        print collName
        with open (filePath, "r") as f:
            file_data = json_util.loads(f.read())

        collName.insert(file_data)
        client.close()        
    except Exception as er:
        print "Exception Error UploadCollection func ===> %s"%er


if __name__ == "__main__":

    mongoIP = sys.argv[1];
    mongoPort = int(sys.argv[2]);
    dbName = sys.argv[3];
    sysPath = sys.argv[4];

    home = expanduser('~')
    path = home + "/" + sysPath +"/"+ dbName
    print "mongodb Connection IP:  %s:%s DbName %s & syspath : %s"%(mongoIP, mongoPort, dbName, path)
    client = MongoClient(mongoIP,mongoPort) #db connectionInitialize
    dbInit = client[dbName]

    py_read_folderfiles(dbInit, dbName, path)

