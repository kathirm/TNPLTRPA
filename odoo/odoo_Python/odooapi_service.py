from flask import Flask
import odoofactory
from flask import jsonify
import json
from configparser import ConfigParser


app = Flask(__name__)
app.config['DEBUG'] = True

cfgFile = '/home/kathir/odoo_Python/odoo.cfg'
config = ConfigParser()
config.read(cfgFile)

#getConfiguration file details
dbIp = config['postgreSql']['ip']
dbPort = config['postgreSql']['port']
dbUser_name = config['postgreSql']['username']
db_pwd = config['postgreSql']['pwd']

#database connection details
database_name = config['database']['dbname']
#Portal_configuration
portal_port = config['portal']['poratal_port']
portal_admin_name = config['portal']['admin_username']

libConnection = odoofactory.odooLibrary(dbIp, dbPort, dbUser_name, db_pwd, database_name, dbIp, portal_admin_name)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/getRecords')
def getuserDetails():
    try:
        recordList  = []
        records = libConnection.get_records()
        for row in records:
            record = {}
            record["userId"] = row[2] 
            record["password"] = row[3]
            recordList.append(record)
    
    except Exception as er:
        print("\n [WARNING] GET ALL ODOO-USERS API FUNCTION EXCEPTION :: %s"%er+'\n')

    return jsonify(recordList=list)


if __name__ == "__main__":
    app.run(host='10.6.7.88', port=8002)
