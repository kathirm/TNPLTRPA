import os, json, sys
from apscheduler.schedulers.background import BackgroundScheduler
import schedule
import time, datetime
from datetime import datetime, timedelta
from configparser import ConfigParser
import psycopg2
from calendar import monthrange

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

print dbIp, dbPort, dbUser_name, db_pwd, database_name

def initMaster_dateabase():
    try:
        conn = None
        conn = psycopg2.connect(database= database_name, user = dbUser_name,
                password = db_pwd, host = dbIp, port = dbPort)
        cur = conn.cursor()
        get_result = cur.execute("SELECT databasename, client_username, created_date FROM res_userinfo")
        result = cur.fetchall()
        subscriRecord = [] 
        for data in result:
            records = {}
            records['dbname'] = data[0]
            records['username'] = data[1]
            records["createdDate"] = data[2][:10]
            subscriRecord.append(records)
        unsubscribe_userslogin(subscriRecord)
    except Exception as er:
        print("[WARNING] MASTER DATABASE CONNECTION EXCEPTION ERROR :: %s"%er)
    return subscriRecord 

def conn_users_database(databasename, username):
    try:
        user_connect = None
        getId = None
        user_connect = psycopg2.connect(database= databasename, user = dbUser_name, password = db_pwd, host = dbIp, port = dbPort)
        cur = user_connect.cursor()
        #getUsre records
        get_ids = cur.execute("SELECT id FROM res_users WHERE login= '%s'"%username)
        result = cur.fetchall()
        for _id in result:
            getId =  _id[0]
    except Exception as er:
        print ("[WARNING] USERS DATABASE CONNECTION EXCEPTION :: %s"%er)
    return user_connect,  getId

def update_subscription_pack(connect, userid):
    try:
        resp = None
        cur = connect.cursor()
        cur.execute("UPDATE res_users SET active = 'false' WHERE id=%s"%(userid))
        connect.commit()
        resp = {"result" : "user blocked successfull"}
    except Exception as er:
        print("UPDATE SUBSCRIBTION EXCEPTION AS ERROR :: %s"%er)
    return resp

def unsubscribe_userslogin(records):
    try:
        today= datetime.strftime(datetime.now() , '%Y-%m-%d')
        cus_today = datetime.strptime(today, "%Y-%m-%d").date()
        for recd in records:
            conn, getId = conn_users_database(recd.get('dbname'), recd.get('username'))
            getdate = recd.get('createdDate')
            cus_date = datetime.strptime(getdate, "%Y-%m-%d").date()
            duration =  (cus_today - cus_date ).days 
            #getCurrent month days
            get_currentyear = datetime.now().strftime('%Y')
            get_currentmonth = current_month = datetime.now().strftime('%m')
            num_days = monthrange(int(get_currentyear), int(get_currentmonth))[1]
            #validate duration time & date
            if int(duration) == int(num_days):
               resp = update_subscription_pack(conn, getId) 
               print resp
            else:
                print "None OF THE USERS FOUND TODAY :: %s"%str(today) 

    except Exception as er:
        print ("[WARNING] UNSUBSCRIBE USERS LOGIN EXCEPTION ERROR :: %s"%er)


scheduler = BackgroundScheduler()
scheduler.start()
job = scheduler.add_job(initMaster_dateabase, 'cron', hour='00', minute='05', second='00')
print"Current job starting....."
while True:
   time.sleep(5)





#initMaster_dateabase()
