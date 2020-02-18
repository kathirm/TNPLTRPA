import json, os, sys, time
from configparser import ConfigParser
import xmlrpclib
import requests
import psycopg2 #Connect postgreSQL database
from passlib.context import CryptContext
import erppeek
import postgreLib
import logging
from utills import *


class odooLibrary:

    def __init__(self, dbIp, dbPort, dbusername = None, dbpwd = None, dbName = None, portal_port = None, admin_name = None):

        self.portal_url = "http://%s:%s"%(dbIp, portal_port)
        logging.basicConfig(level=logging.DEBUG)
        self.dbIp = dbIp;
        self.dbPort = dbPort;
        self.dbusername = dbusername;
        self.dbpwd = dbpwd;
        self.dbName = dbName;
        self.portal_port = portal_port;
        self.admin_name  = admin_name;
        self.defaultpwd = dbpwd; 
        self.connect = None
        self.dbConnection = self.connect_sqldb()
        self.default_package = ["mass_mailing", "board"]

    def connect_sqldb(self):
        try:
            conn = None
            conn = psycopg2.connect(database= self.dbName, user = self.dbusername,
                    password = self.dbpwd, host = self.dbIp, port = self.dbPort)
            self.cur = conn.cursor()
        except Exception as e:
            logging.warning("CONNECT POSTGRESQL DATABASE CONNECTION ERROR ::%s"%e)

        return conn

    def get_records(self):
        try:
            self.cur.execute("SELECT * FROM res_users")
            rows = self.cur.fetchall()
            for row in rows:
                print row

        except Exception as e:
            logging.warning("GET RECORDS FUNCTION EXCEPTION ERROR :: %s"%e)

    def get_databaseNames(self):
        try:
            dblist = None
            client = erppeek.Client(server = self.portal_url)
            dblist = client.db.list();

        except Exception as er:
            logging.warning("[WARNING] GET LIST OF DATABASE NAMES EXCEPTION :: %s"%er)

        return dblist

    def create_newUser_database(self, params):
        try:
            client = None
            resp = None
            DATABASE = params.get("databaseName").upper()
            
            logging.info("CREATE DATABASE INPUT PARAMS VALUE :: %s"%params+'\n')
            client = erppeek.Client(server = self.portal_url)
            #url = client.split("xmlrpc")
            
            if not DATABASE in client.db.list():
                logging.info("THE DATABASE DOES NOT EXIST YET CREATING NEW ONE..!!")
                client.create_database(self.dbpwd, DATABASE)
                logging.info("[SUCCESS] NEW DATABASE " + DATABASE +" CREATED IN ODOO SERVER")
                logging.critical("[ALERT] YOUR DATABASE " + DATABASE + " CONFIGURATION IN-PROGRESS \n PLEASE WAIT...")
                time.sleep(10)
                self.get_newDatabase_admin_id(DATABASE, params)
                self.create_db_sub_users(DATABASE, params)
                resp = {"result" : "Created"} 
            else:
                logging.warning("THE DATABASE " + DATABASE + " ALREADY EXISTS")
                resp = {"result":"database name already exists"}

        except Exception as er:
            logging.warning("CREATE NEW-USER DATABASE FUNCTION EXCEPTION :: %s"%er+'\n')

        return resp 

    def connect_user_database(self, dbName):
        try:
            self.connection  = postgreLib.postgreLib(self.dbIp, self.dbPort, self.dbusername, self.dbpwd, dbName)
            self.connect = self.connection.connect_postgreSQL()

        except Exception as er:
            logging.warning("[WARNING] I AM UNABLE TO CONNECT TO THE POSTGRESQL DATABASE FUNCTION EXCEPTION :: %s"%er)

        return self.connection

    def get_newDatabase_admin_id(self, database, params=None):
        try:
            user_id = None;
            self.connect_user_database(database)
            self.connection_state = self.connect.cursor()

            self.connection_state.execute("SELECT * FROM res_users WHERE login='admin'")
            rows = self.connection_state.fetchall()
            for row in rows:
                user_id = row[0]
            logging.info("[SUCCESS] CURRENT DATABASE NAME : "+ database + " & ADMIN USER ID :: %s"%user_id)

            if user_id is None:
                logging.warning("[WARNING] ADMIN USER NAME NOT FOUND IN CURRENT DATABASE " + database +" TRY AFTER SOMETIME")
            else:
                update_pwd = self.connection.reset_admin_pwd(self.connect, user_id)
                if update_pwd is not None:
                    client = self.install_packages(database, self.default_package)
                else:
                    logging.warning("[WARNING] NEW CREATED DATABASE " + database+ " ADMIN USER PASSWORD UPDATION FAILED")

        except Exception as er:
            logging.warning("[WARNING] CREATED NEW DATABASE " +database+ "FUNCTION EXCEPTION :: %s"%er)

        return user_id

    def install_packages(self, database, install_package):
        try:
            client = None
            module_name = install_package 
            client = erppeek.Client(self.portal_url, database, 'admin', self.defaultpwd)
            proxy = client.model('ir.module.module')
            installed_modules = proxy.browse([('state', '=', 'installed')])

            for module in installed_modules:
                logging.info("[INFO] INSTALLED MODULE: " + module.name)

            for insta_module in module_name:
                modules = client.modules(insta_module, installed=False)
                if insta_module in modules['uninstalled']:
                    client.install(insta_module)
                    logging.info("[SUCCESS] THE MODULE %s HAS BEEN INSTALLED!"%insta_module)
 
        except Exception as er:
            logging.warning("[WARINING] NEW USER INSTALLED PACKAGE EXCEPTION :: %s"%er)

        return client

    def create_db_sub_users(self, database, params=None):
        try:
            user_id = None;
            if params is None:
                logging.warning("[WARNING] INPUT PARAMS VALUE IS NONE PLEASE TRY AGAIN...")
            else:
                insta_module = self.dependancy_package_install_modules(params)
                self.install_packages(database, insta_module)
                package_info = self.installed_package_grouping_for_sub_user(params) 
                client_name = params.get('client_username')
               
                common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.portal_url))
                uid = common.authenticate(database, 'admin', self.dbpwd, {})
                models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.portal_url))

                user_id = models.execute_kw(database, uid, self.dbpwd, 'res.users', 'create',[package_info])
                logging.info('[INFO] CREATE NEW USERNAME IN ODOO COMPLETED:: %s'%user_id)

                if user_id is None:
                    logging.warning("[WARNING] USERNAME or EMAIL ID IS ALREADY EXIST IN ODOO SERVER")
                else:
                    self.connect_user_database(database)
                    update_pwd = self.connection.reset_admin_pwd(self.connect, user_id)
                    if update_pwd is not None:
                        self.create_usrInfoTable(params)
                        email_notification(client_name, body = "Dear Customer <br><br> we are proudly welcome to You <br><br> Your Account has been created succesfully your login Credentials <b><br> user name : %s <br> Password : %s <br></b><br><br> Thanks & Regards<br>STORAZE Support Team"%(client_name, self.defaultpwd))
                    else:
                        logging.warning("[WARNING] E-MAIL NOTIFICATION MAILID NOT FOUND PLEASE TRY AFTER SOME TIME.....")

        except Exception as er:
            logging.warning('[WARNING] CREATE NEW INTERNAL USER FUNCTION EXCEPTION ERROR :: %s'%er)

        return user_id

    def sendFeedbackMail(self, params):
        try:  
            email_notification("mkathir@terafastnet.com", body="Hello  Postmaster </br></br> You have Received one New Feedback Message <br></br> Client Name :: %s <br> Client Company : %s <br> Customer mail-ID : %s <br> Customer Phone Number : %s <br> Message : %s  <br> </br> Thanks & Regards <br> support Team"%(params.get("custName"), params.get("custCompany"), params.get("custEmailAdd"), params.get("custPhone"), params.get("custmsg")))
        except Exception as er:
            print("SEND CUSTOMER FEEDBACK MAIL NOTIFICATION EXCEPTION :: %s"%er)


    def dependancy_package_install_modules(self, params):
        try:
            modules = params.get("productType")
            if len(modules) == 0:
                logging.warning("[WARNING] INPUT PACKAGE PRODUCT TYPES OF VALUES ARE EMPTY...")
            else:
                module = []
                with open('/etc/odoopackage.json') as f:
                    insta_pack = json.load(f)
                    for i in insta_pack:
                        for pack in modules:
                            val = i.get(pack)
                            for ival in val:
                                module.append(ival)
        except Exception as er:
            logging.warning("[WARNING] INSTALL APPLICATION GROUPING FUNCTION EXCEPTION :: %s"%er)
        return module

    def installed_package_grouping_for_sub_user(self,  params):
        try:
            package_info = None
            modules = params.get("productType");
            if len(modules) == 0:
                logging.warning("[WARNING] INPUT PACKAGE PRODUCT TYPES OF VALUES ARE EMPTY...")
            else:
                client_username = params.get('client_name')
                client_name = params.get('client_username')
                client_password = params.get('client_password')

                package_info = {
                         'name': client_username,
                         'login':client_name,
                         'company_ids':[1],
                         'company_id':1,
                         'new_password': client_password,
                         'sel_groups_11' : 11
                        }
                with open('/etc/odoogrouping.json') as f:
                    modules_list = json.load(f) 
                    for pack in modules:
                        for module in modules_list:
                            for key, value in module[pack].items():
                                package_info[key] = value
     
        except Exception as er:
            logging.warning("[WARNING] INSTALLED MODULES PACKAGE GROUPING EXCEPTION :: %s"%er)
        return package_info

    def create_usrInfoTable(self, params):
        try:
            DATABASE = params.get("databaseName").upper()
            self.connection  = postgreLib.postgreLib(self.dbIp, self.dbPort, self.dbusername, self.dbpwd, self.dbName)
            self.connect = self.connection.connect_postgreSQL()
            #self.connection.create_table(self.connect)
            self.connection.insertUsrRecords(self.connect, params)

        except Exception as er:
            logging.warning("[WARNING] CREATE USER INFORMATIONSAVED COLLECTION EXCEPTION :: %s"%er)

    def create_additional_users(self, params=None):
        try:
            resp = None
            DATABASE = params.get("client_name").upper() 
            username = params.get("client_username")

            client = erppeek.Client(server = self.portal_url)

            if DATABASE in client.db.list():
                self.connection  = postgreLib.postgreLib(self.dbIp, self.dbPort, self.dbusername, self.dbpwd, DATABASE)
                self.connect = self.connection.connect_postgreSQL()
                result = self.connection.getRecords(self.connect, DATABASE, "res_users")

                if result is not None:
                    for rows in result:
                        if rows[0] ==  username:
                            resp = {'auth-result': 'Complete'} 
                            break
                    else:
                        resp = {'auth-result': 'Invalid User'}
                else:
                    logging.warning("[WARNING] USER RESULT NOT FOUND IN ODOO")
            else:
                resp = {'auth-result':'Invalid User'}
        except Exception as er:
            logging.warning("[WARNING] CREATE ADDTIONAL USERS EXCEPTION :: %s"%er)
        
        return resp

    def additional_users(self, params):
        try:
            resp = None
            database = params.get("client_name").upper() 
            client_username = params.get("client_subusername") 
            client_name = params.get("client_subusername") 
            client_password = params.get("client_password")
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.portal_url))
            uid = common.authenticate(database, 'admin', self.dbpwd, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.portal_url))

            self.connection  = postgreLib.postgreLib(self.dbIp, self.dbPort, self.dbusername, self.dbpwd, database)
            self.connect = self.connection.connect_postgreSQL()
            user_id = models.execute_kw(database, uid, self.dbpwd, 'res.users', 'create', [{
                'name': client_username,
                'login':client_name,
                'company_ids':[1],
                'company_id':1,
                'new_password': client_password,
                }])
            update_pwd = self.connection.reset_admin_pwd(self.connect, user_id)
            resp = {"auth-result" : "CREATED ID %s"%user_id}
        except Exception as er:
            resp = {"auth-result":"USERNAME ALREADY EXIST"}
            logging.warning("[WARNING] CREATE ADDITIONAL NEW USER EXCEPTION :: %s"%er)

        return resp

    def userLogin(self, params):
        try:
            resp = None
            connection  = postgreLib.postgreLib(self.dbIp, self.dbPort, self.dbusername, self.dbpwd, self.dbName)
            connect = connection.connect_postgreSQL()
            dbName = connection.userLogin(connect, params)
            if dbName is not None:
                resp = dbName[0]
            else:
                resp = "username or password mismatch"

        except Exception as er:
            logging.warning("[WARNING] USERS LOGIN EXCEPTION :: %s"%er)
        return resp




if __name__ == "__main__" :

    cfgFile = '/etc/odoo.cfg'
    config = ConfigParser()
    config.read(cfgFile)

    #getConfiguration file details
    dbIp = config['postgreSql']['ip']
    dbPort = config['postgreSql']['port']
    dbUser_name = config['postgreSql']['username']
    db_pwd = config['postgreSql']['pwd']

    database_name = config['database']['dbname']
    portal_port = config['portal']['poratal_port']
    portal_admin_name = config['portal']['admin_username']

    odooLibrary(dbIp, dbPort, dbUser_name, db_pwd, database_name, portal_port, portal_admin_name)
