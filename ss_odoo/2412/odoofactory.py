import json, os, sys, time
from configparser import ConfigParser
import xmlrpclib
import requests
import psycopg2 #Connect postgreSQL database
from passlib.context import CryptContext
import erppeek
import postgreLib
from utills import *


class odooLibrary:

    def __init__(self, dbIp, dbPort, dbusername = None, dbpwd = None, dbName = None, portal_port = None, admin_name = None):

        self.portal_url = "http://%s:%s"%(dbIp, portal_port)
        self.dbIp = dbIp;
        self.dbPort = dbPort;
        self.dbusername = dbusername;
        self.dbpwd = dbpwd;
        self.dbName = dbName;
        self.portal_port = portal_port;
        self.admin_name  = admin_name;
        self.defaultpwd = "abcd123"
        self.connect = None
        self.dbConnection = self.connect_sqldb()
        self.default_package = ["mass_mailing", "board"]

        #self.create_newUser_database() 
        #self.get_newDatabase_admin_id("TERAFASTNETWORKS")
        self.params  = {
                "client_name": "venky1",
                "client_password": "abcd123",
                "client_username": "imkathir@yahoo.com"
                }
        #self.create_db_sub_users("TERAFASTNETWORKS",self.params)

    def connect_sqldb(self):
        try:
            conn = psycopg2.connect(database= self.dbName, user = self.dbusername,
                    password = self.dbpwd, host = self.dbIp, port = self.dbPort)
            self.cur = conn.cursor()
        except Exception as e:
            print("\n [WARNING] CONNECT POSTGRESQL DATABASE CONNECTION ERROR ::%s"%e)

        return conn

    def get_records(self):
        try:
            self.cur.execute("SELECT * FROM res_users")
            rows = self.cur.fetchall()
            for row in rows:
                print row

        except Exception as e:
            print("\n [WARNING] GET RECORDS FUNCTION EXCEPTION ERROR :: %s"%e)

    def create_newUser_database(self, params=None):
        try:
            client = None
            DATABASE = "TERAFASTNETWORKS"
            print("\n [INFO] CREATE DATABASE INPUT PARAMS VALUE :: %s"%params+'\n')
            client = erppeek.Client(server = self.portal_url)

            if not DATABASE in client.db.list():
                print("\n [INFO] THE DATABASE DOES NOT EXIST YET CREATING NEW ONE..!!")
                client.create_database(self.dbpwd, DATABASE)
                print("\n [SUCCESS] NEW DATABASE " + DATABASE +" CREATED IN ODOO SERVER")
                print("\n [ALERT] YOUR DATABASE " + DATABASE + " CONFIGURATION IN-PROGRESS \n PLEASE WAIT...")
                time.sleep(10)
                self.get_newDatabase_admin_id(DATABASE)
            else:
                print("\n [WARNING] THE DATABASE " + DATABASE + " ALREADY EXISTS")

        except Exception as er:
            print("\n [WARNING] CREATE NEW-USER DATABASE FUNCTION EXCEPTION :: %s"%er+'\n')

        return client

    def connect_user_database(self, dbName):
        try:
            self.connection  = postgreLib.postgreLib(self.dbIp, self.dbPort, self.dbusername, self.dbpwd, dbName)
            self.connect = self.connection.connect_postgreSQL()

        except Exception as er:
            print("\n [WARNING] I AM UNABLE TO CONNECT TO THE POSTGRESQL DATABASE FUNCTION EXCEPTION :: %s"%er)

        return self.connection

    def get_newDatabase_admin_id(self, database):
        try:
            user_id = None;
            self.connect_user_database(database)
            self.connection_state = self.connect.cursor()

            self.connection_state.execute("SELECT * FROM res_users WHERE login='admin'")
            rows = self.connection_state.fetchall()
            for row in rows:
                user_id = row[0]
            print("\n [SUCCESS] CURRENT DATABASE NAME : "+ database + " & ADMIN USER ID :: %s"%user_id)

            if user_id is None:
                print("\n [WARNING] ADMIN USER NAME NOT FOUND IN CURRENT DATABASE " + database +" TRY AFTER SOMETIME")
            else:
                update_pwd = self.connection.reset_admin_pwd(self.connect, user_id)
                if update_pwd is not None:
                    client = self.install_packages(database)
                else:
                    print("\n [WARNING] NEW CREATED DATABASE " + database+ " ADMIN USER PASSWORD UPDATION FAILED")

        except Exception as er:
            print("\n [WARNING] CREATED NEW DATABASE " +database+ "FUNCTION EXCEPTION :: %s"%er)

        return user_id

    def install_packages(self, database, params=None):
        try:
            client = None
            module_name = self.default_package
            client = erppeek.Client(self.portal_url, database, 'admin', self.defaultpwd)
            proxy = client.model('ir.module.module')
            installed_modules = proxy.browse([('state', '=', 'installed')])

            for module in installed_modules:
                print("\n [INFO] INSTALLED MODULE: " + module.name)

            for insta_module in module_name:
                modules = client.modules(insta_module, installed=False)
                if insta_module in modules['uninstalled']:
                    client.install(insta_module)
                    print("\n [SUCCESS] THE MODULE %s HAS BEEN INSTALLED!"%insta_module)
 
        except Exception as er:
            print("\n [WARINING] NEW USER INSTALLED PACKAGE EXCEPTION :: %s"%er)

        return client

    def create_db_sub_users(self, database, params=None):
        try:
            user_id = None;
            if params is None:
                print("\n [WARNING] INPUT PARAMS VALUE IS NONE PLEASE TRY AGAIN...")
            else:
                client_username = params.get('client_name')
                client_name = params.get('client_username')
                client_password = params.get('client_password')

                common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.portal_url))
                uid = common.authenticate(database, 'admin', self.dbpwd, {})
                models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.portal_url))

                user_id = models.execute_kw(database, uid, self.dbpwd, 'res.users', 'create', [{
                    'name': client_username,
                    'login':client_name,
                    'company_ids':[1],
                    'company_id':1,
                    'new_password': client_password,
                    'sel_groups_11' : 11
                                       
                    }])
                print('\n [INFO] CREATE NEW USERNAME IN ODOO COMPLETED:: %s'%user_id)

                if user_id is None:
                    print("\n [WARNING] USERNAME or EMAIL ID IS ALREADY EXIST IN ODOO SERVER")
                else:
                    self.connect_user_database(database)
                    update_pwd = self.connection.reset_admin_pwd(self.connect, user_id)
                    if update_pwd is not None:
                        email_notification(client_name, body = "Your Account has been activated shortly and your login password ::%s<br><br> Thank you :)"%self.defaultpwd)
                    else:
                        print("\n [WARNING] E-MAIL NOTIFICATION MAILID NOT FOUND PLEASE TRY AFTER SOME TIME.....")

        except Exception as er:
            print('\n [WARNING] CREATE NEW INTERNAL USER FUNCTION EXCEPTION ERROR :: %s'%er)

        return user_id


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
