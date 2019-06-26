import json, sys
from pymongo import MongoClient
from bson import json_util


def ExportData():    
    client = MongoClient('157.230.255.60',37017)
    db = client['Kalakshetra']
    collName = db['reportConfig']

    with open('/home/mravi/157.230.255.60/Kalakshetra/reportConfig.json') as f:
        file_data = json_util.loads(f.read())

    collName.insert(file_data)
    client.close()

if __name__ == "__main__":

    ExportData()
