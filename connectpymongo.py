import pymongo, sys, json
from bson.json_util import dumps
from os.path import join


dbName = sys.argv[1]
client = pymongo.MongoClient('mongodb://userAdmin:terafastnetworks@'+ "159.65.157.226", 37017)
database = client[dbName]
collections = database.collection_names()

print collections
for i, collection_name in enumerate(collections):
    col = getattr(database,collections[i])
    collection = col.find()

    print collection
    outputs_dir = "/home/kathir/"
    jsonpath = collection_name + ".json"
    jsonpath = join(outputs_dir, jsonpath)
    with open(jsonpath, 'wb') as jsonfile:
        jsonfile.write(dumps(collection))

