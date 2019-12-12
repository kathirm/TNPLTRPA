import json, os, sys
from configparser import ConfigParser
import xmlrpclib
import requests
import psycopg2
from passlib.context import CryptContext
from utils import *

class odooLibrary:

    def __init__(self, dbIp, dbPort, dbusername = None, dbpwd = None, dbName = None, portal_port = None, admin_name = None):

        self.dbIp = dbIp;
        self.dbPort = dbPort;
        self.dbusername = dbusername;
        self.dbpwd = dbpwd;
        self.dbName = dbName;
        self.portal_port = portal_port;
        self.admin_name  = admin_name;
        self.defaultpwd = "abcd123" 
        self.dbConnection = self.connect_sqldb()
        self.portal_url = "http://%s:%s"%(dbIp, portal_port)
        self.params  = {
                        "client_name": "venky1",
                        "client_password": "abcd123", 
                        "client_username": "imkathir@yahoo.com"
                      }
        #self.create_admin_subUsers(self.params)

        self.forgot_and_reset_pwd("mkathir@terafastnet.com")
        #self.create_new_admin_user(self.params)
    
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


    def create_admin_subUsers(self, params):
        try:
            user_id = None;
            if params is None:
                print("\n [WARNING] INPUT PARAMS VALUE IS NONE PLEASE TRY AGAIN...")
            client_username = params.get('client_name')
            client_name = params.get('client_username')
            client_password = params.get('client_password')

            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.portal_url))
            uid = common.authenticate(self.dbName, self.admin_name, self.dbpwd, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.portal_url))

            user_id = models.execute_kw(self.dbName, uid, self.dbpwd, 'res.users', 'create', [{
                'name': client_username,
                'login':client_name,
                'company_ids':[1],
                'company_id':1,
                'new_password': client_password
                }])
            print('\n [INFO] CREATE NEW USERNAME IN ODOO COMPLETED:: %s'%user_id)

            if user_id is None:
                print("\n [WARNING] USERNAME or EMAIL ID IS ALREADY EXIST IN ODOO SERVER")
            else:
                resp = self.reset_user_pwd(user_id)
                if resp is not None:
                    email_notification(client_name, body = "Your Account has been activated shortly and your login password ::%s<br><br> Thank you :)"%self.defaultpwd)
                else:
                    print("\n [WARNING] E-MAIL NOTIFICATION MAILID NOT FOUND PLEASE TRY AFTER SOME TIME.....")
                

        except Exception as er:
            print('\n [WARNING] CREATE NEW INTERNAL USER FUNCTION EXCEPTION ERROR :: %s'%er)

        return user_id

    def reset_user_pwd(self, user_id):
        try:
            newpass_crypt = None;
            newpass_crypt = CryptContext(['pbkdf2_sha512']).encrypt(self.defaultpwd)
            self.cur.execute("UPDATE res_users SET password = '"+newpass_crypt+"' WHERE id=%s"%(user_id))
            self.dbConnection.commit()
            self.dbConnection.close()
            print("\n [SUCCESS] PASSWORD FOR USERID :: %s HAS BEEN UPDATED SUCCESSFULLY"%user_id)

        except Exception as er:
            print("\n [WARNING] CREATED USERID :: %s  PASSWORD RESET FUNCTION ERROR ::%s"%(user_id, er))

        return newpass_crypt


    def create_new_admin_user(self, params):
        try:
            user_id = None;
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.portal_url))
            uid = common.authenticate(self.dbName, self.admin_name, self.dbpwd, {})
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.portal_url))

            client_username = params.get("client_username")
            client_name = params.get("client_name")
            client_password = params.get("client_password")

            user_id  = models.execute_kw(self.dbName, uid, self.dbpwd, 'res.users', 'signup', [{
                'login': client_username,
                'name': client_name,
                'password': client_password
                }])
            print('\n [INFO] CREATE NEW USERNAME IN ODOO COMPLETED:: %s'%user_id)

            if user_id is None:
                print("\n [WARNING] USERNAME or EMAIL ID IS ALREADY EXIST IN ODOO SERVER")

        except Exception as er:
            print("\n [WARNING] CREATE NEW ADMIN USER FUNCTION EXCEPTION :: %s"%er)

        return user_id

    def forgot_and_reset_pwd(self, usr_mail):
        try:
            rows = None;
            self.cur.execute("SELECT * FROM res_users WHERE login = '%s'"%usr_mail)
            rows = self.cur.fetchall()
            if len(rows) == 0:
                print("\n [WARNING] FORGOT PASSWORD EMAIL ID { %s } IS NOT FOUND"%usr_mail.upper())
            for row in rows:
                usr_id = row[0]
                resp = self.reset_user_pwd(usr_id)
                if resp is not None:
                    email_notification(usr_mail, body = "Your Account has been activated shortly and your login password ::%s<br><br> Thank                                       you :)"%self.defaultpwd)
                    print("\n [SUCCESS] YOUR FORGOT PASSWORD CHANGED PLEASE CHECK EMAIL ID :: %s"%usr_mail.upper()+'\n') 
                else:
                    print("\n [WARNING] FORGOT PASSWORD USER EMAIL ID NOT FOUND")

        except Exception as er:
            print("\n [WARNING] USER FORGOT PASSWORD EXCEPTION ERROR :: %s"%er)

        return rows



if __name__ == "__main__" :

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

    odooLibrary(dbIp, dbPort, dbUser_name, db_pwd, database_name, portal_port, portal_admin_name)
