import json, os, sys, time
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
            print("\n [SUCCESS] PASSWORD TO USERID :: %s HAS BEEN UPDATED SUCCESSFULLY"%user_id)
        except Exception as er:
            print("\n [WARNING] CREATED USERID :: %s  PASSWORD RESET FUNCTION ERROR ::%s"%(user_id, er))

        return newpass_crypt
