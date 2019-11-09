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

    if len(sys.argv) != 5:
        print "Usage: %s <1.ExportDBIp, 2.Port, 3.DbName, 4.SysPath>" % (sys.argv[0])
        sys.exit(0);

    mongoIP = sys.argv[1];
    mongoPort = int(sys.argv[2]);
    dbName = sys.argv[3];
    sysPath = sys.argv[4];

    home = expanduser('~')
    path = home + "/" + sysPath +"/"+ dbName 
    print "mongodb Connection IP:  %s:%s DbName %s & syspath : %s"%(mongoIP, mongoPort, dbName, path)
    client = MongoClient('mongodb://userAdmin:terafastnetworks@'+ mongoIP,mongoPort) #db connectionInitialize
    #client = MongoClient(mongoIP,mongoPort)
    dbInit = client[dbName]

    py_read_folderfiles(dbInit, dbName, path)

