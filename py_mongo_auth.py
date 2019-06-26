import json, os, sys
from pymongo import MongoClient
import pymongo

def mongo_auth():
    try:
        conn = pymongo.MongoClient('mongodb://xxxxxxxxxxxxx:xxxxxxxx@1111111.11111.111111:111.111.4111')
#       client = MongoClient('mongodb://:'); 
        db = conn["Superstar"]
        colName = db["ObjectRepos"]
        query = {"objectType" : "Json"}
        getRecords = colName.find(query).count()
        print getRecords 
    except Exception as er:
        print "MongoDB %s"%er


mongo_auth()

