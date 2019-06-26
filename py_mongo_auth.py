import json, os, sys
from pymongo import MongoClient
import pymongo

def mongo_auth():
    try:
        conn = pymongo.MongoClient('mongodb://userAdmin:terafastnetworks@10.6.7.28:27017')
#       client = MongoClient('mongodb://userAdmin:terafastnetworks@10.6.7.28:27017'); 
        db = conn["Superstar"]
        colName = db["ObjectRepos"]
        query = {"objectType" : "Json"}
        getRecords = colName.find(query).count()
        print getRecords 
    except Exception as er:
        print "MongoDB %s"%er


mongo_auth()

