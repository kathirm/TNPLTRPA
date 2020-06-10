import os, json, sys
import time, datetime
from datetime import datetime, timedelta
from configparser import ConfigParser
import psycopg2

#Read configuration
cfgFile = '/etc/odoo.cfg'
config = ConfigParser()
config.read(cfgFile)
#database settings
dbIp = config['postgreSql']['ip']
dbPort = int(config['postgreSql']['port'])
dbUser_name = config['postgreSql']['username']
db_pwd = config['postgreSql']['pwd']
database_name = config['database']['dbname']

#print dbIp, dbPort, dbUser_name, db_pwd, database_name

def init_master_database(client_emailid):
    try:
        conn = None
        conn = psycopg2.connect(database= database_name, user = dbUser_name,
                password = db_pwd, host = dbIp, port = dbPort)
        cur = conn.cursor()
        get_result = cur.execute("SELECT databasename FROM res_userinfo WHERE client_username = '%s'"%client_emailid.lower())
        result = cur.fetchall()
        if len(result) == 0:
            print "[WARNING] Invalid Username Or Username Not-found Please Check"
        else:
            for dbName in result:
                database = dbName[0]
                user_account_flag_activation(database, client_emailid)
                updatemaster_database_createdDate(conn, client_emailid)
    except Exception as er:
        print("[WARNING] INIT MASTER DATABASE CONNFIGURATION EXCEPTION AS ERROR :: %s"%er)

def user_account_flag_activation(database, user_id):
    try:
        conn = None
        conn = psycopg2.connect(database= database, user = dbUser_name,
                password = db_pwd, host = dbIp, port = dbPort)
        cur = conn.cursor()
        get_result = cur.execute("SELECT *  FROM res_users WHERE login = '%s'"%user_id.lower())
        result = cur.fetchall()
        for _id in result:
            get_id = _id[0]
            resp = update_account_flag_value(get_id, conn)
            print("[INFO] MESSAGE :: %s"%resp)

    except Exception as er:
        print("USER ACCOUNT FLAG ACTIVATION EXCEPTION AS ERROR :: %s"%er)

def update_account_flag_value(user_id, conn):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE res_users SET active = 'true' WHERE id=%s"%(user_id))
        conn.commit()
        msg = "User id %s is activated"%str(user_id)
        resp = {"result" : msg}
    except Exception as er:
        print("[WARNING] UPDATE USER FLAG EXCEPTION AS ERROR :: %s"%er)

    return resp


def updatemaster_database_createdDate(conn, username):
    try:
        cur = conn.cursor()
        get_result = cur.execute("SELECT id, client_username, created_date FROM res_userinfo WHERE client_username = '%s'"%username.lower())
        result = cur.fetchall()
        for data in result:
            current_userid = data[0]
            resp = update_created_date(conn, current_userid)
            print("[INFO] MESSAGE :: %s"%resp)
            
    except Exception as er:
        print("[WARNING] UPDATE MASTER DATABASE CREATED DATE EXCEPTION AS ERROR :: %s"%er)

def update_created_date(conn, user_id):
    try:
        cur = conn.cursor()
        update_dt = datetime.now()
        cur.execute("UPDATE res_userinfo SET created_date = '%s' WHERE id=%s"%(update_dt, user_id))
        conn.commit()
        resp = {"result" : "Master database Created Date updated Successfully"}
    except Exception as er:
        print("UPDATE CREATED DATE FUNCTION EXCEPTION AS ERROR :: %s"%er)

    return resp


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <Please Input your <Client Email-ID>>" % (sys.argv[0])
        sys.exit(0);
    client_emailid = sys.argv[1]
    init_master_database(client_emailid)
