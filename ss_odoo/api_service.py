from flask import Flask, request
from flask import jsonify
import json
from configparser import ConfigParser
import odoofactory
import make_payment
import postgreLib

app = Flask(__name__)
app.config['DEBUG'] = True 

cfgFile = '/etc/odoo.cfg'
config = ConfigParser()
config.read(cfgFile)

dbIp = config['postgreSql']['ip']
dbPort = int(config['postgreSql']['port'])
dbUser_name = config['postgreSql']['username']
db_pwd = config['postgreSql']['pwd']

database_name = config['database']['dbname']
portal_port = int(config['portal']['poratal_port'])
portal_admin_name = config['portal']['admin_username']

MerchantId = config["payload"]["MerchantId"]
MerchantKey = config["payload"]["MerchantKey"]
url = config["payload"]["url"]
odoo_libConn = odoofactory.odooLibrary(dbIp, dbPort, dbUser_name, db_pwd, database_name, portal_port, portal_admin_name)
payload_cont = make_payment.make_payment(MerchantId, MerchantKey, url)
postgreConn = postgreLib.postgreLib(dbIp, dbPort, dbUser_name, db_pwd, database_name) 
#conn = postgreConn.connect_postgreSQL()
#info_coll = postgreConn.create_table(conn)
#collection =  postgreConn.create_paymentTable(conn)

@app.route('/')
def hello_world():
    return jsonify({"version":1.0}) 

def masterDbConn():
    try:
        conn = None
        postgreConn = postgreLib.postgreLib(dbIp, dbPort, dbUser_name, db_pwd, database_name)
        conn = postgreConn.connect_postgreSQL()

    except Exception as er:
        print"[WARNING] CONNECT MASTER DATABASE FUNCTION EXCEPTION :: %s"%er

    return conn

@app.route('/createuser', methods=['POST'])
def create_user_database():
    try:
        if request.method == 'POST': 
            resp = None
            respData = json.loads(request.get_json())
            #respData = request.get_json()
            conn = masterDbConn()
            merOrderId = postgreConn.getMerchantOrderId(conn)
            if merOrderId is not None:
                inputData = respData
                inputData["merchantOrderId"] = merOrderId
                resp = payload_cont.payload_form(inputData)
                return_code = resp.get("ReturnCode")
                if str(return_code) == "0":
                    que = postgreConn.storedMerchantReturnResp(conn, resp)
                    resp = odoo_libConn.create_newUser_database(respData)
                else:
                    resp = resp
                    que = postgreConn.storedMerchantReturnResp(conn, resp)
            else:
                resp = {"Message": "MerchantOrderId  is required"}
        else:
            print("\n [WARNING] API-CALL SERVICE METHOD INVALID")

    except Exception as er:
        print("\n [WARNING] CREATE USER-DATABASE API SERVICE EXCEPTION :: %s"%er)

    return jsonify(resp)


@app.route('/saveusrInfo', methods=['POST'])
def create_userInfoTable():
    try:
        if request.method == 'POST':
            params = request.get_json()
            #respdata = json.loads(request.get_json()) 
            resp = odoo_libConn.create_usrInfoTable(params)
        else:
            print("\n [WARNING] METHOD NOT SUPPORTED IN REQUEST SERVICE")

    except Exception as er:
        print("\n [WARNING] CREATE USER INFORMATION TABLE API_SERVICE EXCEPTION :: %s"%er)

    return "waiting"

@app.route('/validateuser', methods=['GET', 'POST'])
def additional_users():
    try:
        if request.method ==  'POST':
            #resp_data = request.get_json()
            resp_data = json.loads(request.get_json())
            resp = odoo_libConn.create_additional_users(resp_data)
    except Exception as er:
        print("\n [WARNING] CREATE ADDITIONAL USERS EXCEPTION ERROR :: %s"%er)

    return jsonify(resp)

@app.route('/addonusers', methods=['GET', 'POST'])
def addonUsers():
    try:
        resp = None
        if request.method == 'POST':
            #resp_data = request.get_json()
            resp_data = json.loads(request.get_json())
            resp = odoo_libConn.additional_users(resp_data)
        else:
            resp = {"result" : "Unsupported  method"}

    except Exception as er:
        print("\n [WARNING] ADDONUSERS CREATE EXCEPTION ERROR :: %s"%er)

    return jsonify(resp)

@app.route('/login', methods=['GET', 'POST'])
def userLogin():
    try:
        resp = None
        if request.method == 'POST':
            #resp = request.get_json() 
            resp = json.loads(request.get_json()) 
            data  = odoo_libConn.userLogin(resp)
            if data is not None:
                resp  = {'result' : data}
            else:
                resp = {'result' : 'username or password mismatch'}
        else:
            resp = {"result":"Unsupported method"}

    except Exception as er:
        print("[WARNING] USER LOGIN EXCEPTION ERROR :: %s"%er)
    return resp

@app.route('/getdblist', methods=['GET', 'POST'])
def getdbList():
    try:
        dblist = None
        dblist = odoo_libConn.get_databaseNames()
        resp = {"database": dblist}
    except Exception as er:
        print "[WARNING] GET DATABASE NAME LIST EXCEPTION ::%s"%er
    return jsonify(resp)

@app.route('/sendmail', methods=["GET", "POST"])
def sendmail():
    try:
        if request.method == "POST":
            resp = json.loads(request.get_json()) 
            odoo_libConn.sendFeedbackMail(resp)
	else:
            print"UN-Suppoted Method"

    except Exception as er:
        print "SEND MAIL NOTIFICATION FUNCTION API SERVICE ERROR :: %s"%er
    return "SUCCESS"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002)
