import json, os, sys, time
import psycopg2
from passlib.context import CryptContext
import logging
from datetime import datetime

class postgreLib:

    def __init__(self, host, port, username, pwd, dbName):
        
        logging.basicConfig(level=logging.DEBUG)
        self.host = host;
        self.port = port;
        self.usrName = username;
        self.pwd = pwd;
        self.dbName = dbName;
        self.defaultpwd = pwd;
        self.dt = datetime.now()
        self.res_usrinfo = "res_userinfo"


    def connect_postgreSQL(self):
        try:
            connection = None;
            connection = psycopg2.connect(database=self.dbName, user = self.usrName, password = self.pwd,
                    host = self.host, port = self.port)
            logging.info("[INFO] NOW YOU ARE CONNECTED WITH " + self.dbName + " DATABASE")

        except Exception as er:
            logging.warning("[WARNING] I AM UNABLE TO CONNECT TO THE POSTGRESQL DATABASE FUNCTION EXCEPTION :: %s"%er)

        return connection

    def reset_admin_pwd(self, conn, user_id):
        try:
            newpass_crypt = None;
            newpass_crypt = CryptContext(['pbkdf2_sha512']).encrypt(self.defaultpwd)
            self.cur = conn.cursor()
            self.cur.execute("UPDATE res_users SET password = '"+newpass_crypt+"' WHERE id=%s"%(user_id))
            conn.commit()
            logging.info("[SUCCESS] PASSWORD TO USERID :: %s HAS BEEN UPDATED SUCCESSFULLY"%user_id)
        except Exception as er:
            logging.warning("[WARNING] CREATED USERID :: %s  PASSWORD RESET FUNCTION ERROR ::%s"%(user_id, er))

        return newpass_crypt


    def create_table(self, conn):
        try:
            logging.info("[INFO] CREATE "+self.res_usrinfo + " IN DATABASE" + self.dbName)
            self.cursor = conn.cursor()
            if self.cursor is not None:
                self.cursor.execute("CREATE TABLE %s(id serial PRIMARY KEY, client_name varchar, databaseName varchar, client_password varchar, productType varchar, totalAmount integer, CardNumber varchar, cardHolderName varchar, expiredMonth varchar, expiredYear integer, cardCVV integer, client_username varchar, created_date varchar)"%self.res_usrinfo)
                conn.commit()
                logging.info("[INFO] USERS BASIC INFO TABLE CREATED INTO "+ self.dbName + " DATABASE...")
            else:
                logging.info("[WARNING] COULD NOT CREATE TABLE IN CURRENT DATABASE :: %s"%self.dbName)
        except Exception as er:
            logging.warning("[WARNING] CREATE USER TABLE IN NEW DATABASE EXCEPTION :: %s"%er)

    def create_paymentTable(self, conn):
        try:
            self.cur = conn.cursor()
            if self.cur is not None:
                self.cur.execute("CREATE TABLE res_payload(id serial PRIMARY KEY, paymentID varchar, tId varchar, returnCode varchar, cardNo varchar, date varchar)")
                conn.commit()
                conn.close()
                logging.info("[INFO] PAYMENT GATEWAY INFORMATION STORED COLLECTION CREATED")
        except Exception as er:
            logging.warning("[WARNING] CREATE PAYMENT GATEWAY INFO TABLE EXCEPTION :: %s"%er)

    def insertUsrRecords(self, conn, params=None):
        try:
            if params is not None:
                modules = params.get("productType")
                productType = ''.join(modules)
                cur = conn.cursor()
                query = "INSERT INTO " + self.res_usrinfo +" (client_name, databaseName, client_password, productType, totalAmount, CardNumber, cardHolderName, expiredMonth, expiredYear, cardCVV, client_username, created_date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(params.get('client_name'), params.get('databaseName'), params.get('client_password'), productType, params.get('totalAmount'), params.get('CardNumber'), params.get('cardHolderName'), params.get('expiredMonth'), params.get('expiredYear'), params.get('cardCVV'), params.get('client_username'), str(self.dt))
                cur.execute(query)
                conn.commit()
                logging.info("[SUCCESS] YOUR LATEST USER DETAILS SAVED INTO DATABASE :: "+self.dbName+" AND TABLENAME " + self.res_usrinfo)

        except Exception as er:
            logging.warning("[WARNING] SAVED INTO USER BASIC INFORMATION EXCEPTION :: %s"%er)

    def getRecords(self, conn, dbname, collectionName):
        try:
            result = None
            cursor = conn.cursor()
            get_result = cursor.execute("SELECT login,password FROM %s"%collectionName)
            result = cursor.fetchall()

        except Exception as er:
            logging.warning("[WARNING] CURRENT DATABASE %s EXCEPTION :: %s"%(dbname, er))

        return result

    def getMerchantOrderId(self, conn):
        try:
            orderId = None
            dt = datetime.now()
            orderId = dt.strftime("%d%m%H%M%Y%S") 

            #cursor = conn.cursor()
            #get_result = cursor.execute("SELECT * FROM res_payload")
            #result = cursor.fetchall()

            #print len(result)
            #if len(result) == 0:
            #    orderId = 1
            #else:
            #    orderId = len(result) +1
        except Exception as er:
            logging.warning("[WARNING] GET MERCHANTORDER ID EXCEPTION :: %s"%er)

        return orderId 

    def storedMerchantReturnResp(self, conn, params):
        try:
            query = None
            cur = conn.cursor()
            query = "INSERT INTO res_payload (paymentid, tid, returncode, cardno, date) VALUES('%s', '%s', '%s', '%s', '%s')"%(params.get('PaymentId'), params.get("Tid"), params.get("ReturnCode"), params.get('cardNumber'), params.get('ReceivedDate'))
            cur.execute(query)
            conn.commit()

        except Exception as er:
            logging.warning("[WARNING] STORED MERCHANT-ID EXCEPTION :: %s"%er)

        return query

    def userLogin(self, conn, param):
        try:
            resp = None
            cur = conn.cursor()
            client_name = param.get("client_name")
            que = cur.execute("SELECT databasename FROM %s WHERE client_username = '%s'"%(self.res_usrinfo, client_name))
            result = cur.fetchall()
            if len(result) == '0':
                resp = {"result" : "not found"}
            else: 
                resp =  result[0]
           
        except Exception as er:
            logging.warning("USERs LOGIN VALIDATION EXCEPTION :: %s"%er)

        return resp
