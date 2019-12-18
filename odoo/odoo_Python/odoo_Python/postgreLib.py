import json, sys
import psycopg2
from passlib.context import CryptContext


class postgreLib:

    def __init__(self, host, port, username, pwd, dbName):

        self.host = host;
        self.port = port;
        self.usrName = username;
        self.pwd = pwd;
        self.dbName = dbName;
        self.defaultpwd = "abcd123";
        self.res_userTable = "res_user_info";

    def connect_postgreSQL(self):
        try:
            connection = None;
            connection = psycopg2.connect(database=self.dbName, user = self.usrName, password = self.pwd, 
                    host = self.host, port = self.port)

            print("\n [INFO] NOW YOU ARE CONNECTED WITH " + self.dbName + " DATABASE")

        except Exception as er:
            print("\n [WARNING] I AM UNABLE TO CONNECT TO THE POSTGRESQL DATABASE FUNCTION EXCEPTION :: %s"%er)

        return connection

    def reset_admin_pwd(self, conn, user_id):
        try:
            newpass_crypt = None;
            newpass_crypt = CryptContext(['pbkdf2_sha512']).encrypt(self.defaultpwd)
            self.cur = conn.cursor()
            self.cur.execute("UPDATE res_users SET password = '"+newpass_crypt+"' WHERE id=%s"%(user_id))
            conn.commit()
            #conn.close()
            print("\n [SUCCESS] PASSWORD TO USERID :: %s HAS BEEN UPDATED SUCCESSFULLY"%user_id)

        except Exception as er:
            print("\n [WARNING] CREATED USERID :: %s  PASSWORD RESET FUNCTION ERROR ::%s"%(user_id, er))

        return newpass_crypt


    def create_table(self, conn):
        try:
            print("\n [INFO] CREATE " + self.res_userTable +" IN DATABASE " +self.dbName )
            self.cur = conn.cursor()
            if self.cur is None:
                print("\n [WARNING] CREATE USER's INFO TABLE CONNECTION EXIST...!")
            else:
                self.cur.execute("CREATE TABLE %s(id serial PRIMARY KEY, customerName varchar, databaseName varchar, customerPwd varchar, productType varchar, totalAmount integer, CardNumber varchar, cardHolderName varchar, expiredMonth varchar, expiredYear integer, cardCVV integer, customerEmail varchar)"%self.res_userTable)
                conn.commit()
                print("\n [SUCCESS] USERS BASIC INFO TABLE CREATED INTO "+ self.dbName + " DATABASE...")

        except Exception as er:
            print("\n [WARNING]  CAN'T DROP OUR " + self.dbName + " DATABASE! AND :: %s"%er)

    def insert_user_info(self, conn, params=None):
        try:
            if params is not None:
                cur = conn.cursor()
                query = "INSERT INTO " + self.res_userTable +" (customerName, databaseName, customerPwd, productType, totalAmount, CardNumber, cardHolderName, expiredMonth, expiredYear, cardCVV, customerEmail) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(params.get('customerName'), params.get('databaseName'), params.get('customerPwd'), params.get('productType'), params.get('totalAmount'), params.get('CardNumber'), params.get('cardHolderName'), params.get('expiredMonth'), params.get('expiredYear'), params.get('cardCVV'), params.get('customerEmail'))
                cur.execute(query)
                conn.commit()
                print("\n [SUCCESS] YOUR LATEST USER DETAILS SAVED INTO DATABASE :: "+self.dbName+" AND TABLENAME " + self.res_userTable)

        except Exception as er:
            print("\n [WARNING] INSERT INTO USER's BASIC INFORMATION " + self.dbName + " AND testQue EXCEPTION :: %s"%er)


