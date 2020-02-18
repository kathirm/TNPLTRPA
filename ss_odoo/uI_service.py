from flask import Flask, request, render_template
import requests, json
from flask import flash
from flask import jsonify,redirect
from configparser import ConfigParser

app = Flask(__name__,template_folder='template', static_folder = "template/img")
app.config['DEBUG'] = True
cfgFile = '/etc/uiConf.cfg'
config = ConfigParser()
config.read(cfgFile)

host = config['redirect']['host']
port = int(config['redirect']['port'])
server = "http://%s:%s"%(host, port)

odooHost = config["odoopage"]["host"]
odooPort = int(config["odoopage"]["port"])
odooserver = "http://%s:%s"%(odooHost, odooPort)


@app.route('/login',methods=['POST','GET'])
def odooLogin():
    try:
        loginPage = "odoo_login.html"
        return render_template(loginPage, message = "welcome")
    except Exception as er:
        print"[WARNING] ODOO LOGIN PAGE RENDERING EXCEPTION :: %s"%er

@app.route('/odoologin', methods=['POST', 'GET'])
def login():
    try:
        resp = None
        if request.method =='POST':
            client_mail = request.form["email"].lower()
            kwargs = {
                    'client_name' : client_mail,
                    'client_pwd'  : request.form["password"]
                    }
            data = json.dumps(kwargs)
            resp = requests.post(server+'/login', json=data)
            resp = json.loads(resp.text)
            if resp['result'] == "username or password mismatch":
                return render_template("odoo_login.html", err="Invalid Username or Password")                 
            else:
                currentdb = requests.get(server+'/getdblist')
                dbs = json.loads(currentdb.text)
                redirec_dbName = resp['result'].upper()
                if redirec_dbName in dbs['database']:
                    resp = odooserver+"/web?db=%s"%redirec_dbName
                else:
                    return render_template("odoo_login.html", err= "You are not ODOO Customer Please Try some time")
        else:
            return render_template("odoo_login.html") 

    except Exception as er:
        print("[WARNING] ODOO LOGIN RESPONSE EXCEPTION :: %s"%er)
        return render_template("odoo_login.html", err="The server is currently Unavailable")
    return redirect(resp) 

@app.route('/', methods=['POST', 'GET'])
def payment_gateway():
    return render_template("Mainscreen.html")
     #return render_template("payment_gatway.html")

@app.route('/validateUser', methods=["POST", 'GET'])
def validate_user():
    return render_template("validate_user.html")

@app.route('/userInputData', methods=['POST', 'GET'])
def userInputData():
    try:
        if request.method == "POST":
            client_username = request.form["email"].lower()
            kwargs = {
                    "client_name" : client_username ,
                    "client_pwd" : request.form["password"] 
                    }

            data = json.dumps(kwargs)
            data = requests.post(server+'/login', json=data)
            userdbName = json.loads(data.text)
            currentdb = requests.get(server+'/getdblist')
            dbs = json.loads(currentdb.text)
            if userdbName["result"] in dbs['database']:
                return render_template("add_subUsers.html", username = userdbName["result"])                
            else:
                return render_template("validate_user.html", err = userdbName["result"])
        else:
            return render_template("validate_user.html")

    except Exception as er:
        print "USER VALIDATATION INPUTDATA EXCEPTION :: %s"%er
    return render_template("validate_user.html")

@app.route('/addonsubusers', methods=['POST', 'GET'])
def  addonsubusers():
    try:
        if request.method=='POST':
            client_subusername =  request.form["email"].lower()
            client_name  = request.form["username" ].upper()
            kwargs = {
                    'client_name' : client_name, 
                    'client_subusername' : client_subusername,
                    'client_password' : request.form['password']
                    }
            data = json.dumps(kwargs)
            response = requests.post(server+"/addonusers", json=data)
            resp = json.loads(response.text)
            auth_result = resp["auth-result"]
            if resp is None:
                return render_template("validate_user.html")
            elif auth_result[:7] == "CREATED":
                resp = odooserver+"/web?db=%s"%client_name.upper()
            elif "USERNAME ALREADY EXIST" in resp["auth-result"]:
                return render_template("validate_user.html", err = resp["auth-result"])
            else:
                return render_template("add_subUsers.html")
        else:
            return render_template("add_subUsers.html")

    except Exception as er:
        print "ADD ON USERS CREATION EXCEPTION :: %s"%er
    return redirect(resp) 

@app.route("/sendmail", methods=["POST", "GET"])
def send_mail():
    try:
        if request.method == "POST":
	    kwargs = {
	            "custName" : request.form["name"],
		    "custCompany" : request.form["company"],
	            "custEmailAdd" : request.form["mail"],
		    "custPhone" : request.form['phoneNumber'],
		    "custmsg" : request.form['message']
		}
	    data = json.dumps(kwargs)
            resp = requests.post(server +'/sendmail', json=data)
	else:
            print"GET METHOD NOT SUPPORTED THIS FUNCTION"
	
    except Exception as er:
        print("SEND MAIL NOTIFICATION FUNCTION EXCEPTION ERROR :: %s"%er)
    return render_template("Mainscreen.html") 

@app.route("/paymentscreen", methods=["POST", "GET"])
def paymentscreen():
    return render_template("payment_gatway.html")

@app.route('/payment', methods=["POST", 'GET'])
def payment():
    try:
        if request.method == 'POST':
            getCust_name = request.form["fullname"].upper();
            cust_name = getCust_name.replace(" ", "")
            cust_email = request.form["customerEmail"].lower()
            kwargs = {
                    "client_name" : cust_name, 
                    "databaseName": cust_name,
                    "client_password" : "Terafast@123",
                    "client_username" : cust_email, 
                    "productType" : request.form.getlist('productType'),
                    "totalAmount" : request.form["totalAmount"], 
                    "CardNumber" : request.form["CardNumber"],
                    "cardHolderName" : request.form["cardholder"],
                    "expiredMonth" : request.form["expiredMonth"],
                    "expiredYear"  : request.form["expiredYear"],
                    "cardCVV"  : request.form["cardCVV"],
                    "customerEmail" : cust_email 
                    }
            resp = requests.get(server+'/getdblist')
            current_dbs = json.loads(resp.text)
            if cust_name in current_dbs["database"]:
                return render_template("payment_gatway.html", err="USERNAME/EMAIL-ID ALREADY EXIST")
            else:
                data = json.dumps(kwargs)
                response = requests.post(server+'/createuser', json=data)
                resp = json.loads(response.text)
                if resp is None:
                    return render_template("payment_gatway.html", err="Invalid credit/debit card details so please check your valid card number(or)security code(cvv) then try again...")
                elif (resp["result"]== "Created"):
                    resp = odooserver+"/web?db=%s"%cust_name.upper()
                else:
                    return render_template("payment_gatway.html", err=resp)
        else:
            return render_template("payment_gatway.html")

    except Exception as er:
        return render_template("payment_gatway.html", err=resp)
    return redirect(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4200)
