import json, os, sys
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler
import requests

def login(job):
    try:
        host = job["host"];
        port = job["port"];
        userName = job["userName"];
        token = None;
        Requrl = "%s:%s"%(host, port)
        Password = "!changeme!"
        login_url = "http://" + Requrl + "/auth/login?username=Admin@%s&password=%s" %(userName, Password)
        headers = []
        token = requests.get(login_url, headers)
        if token.text is not None:
            token_dict= json.loads(token.text)
            if 'access-token' in token_dict:
                token = token_dict['access-token']
                print "retrived token for the user " + userName + " with token: " + token
        gen_attendacne = attendance(Requrl, token);
    except Exception as er:
        print "login Exception as Error :: %s"%(er)
    return token;

def attendance(Requrl, token):
    try:
        empNames = []
        attachments = {}
        sterdaydate = dt.datetime.today() #- dt.timedelta(days=1)
        yesterday = sterdaydate.strftime ('%d-%m-%Y') #get yesterday date
        headers = {"Authorization" : "Bearer %s " %token, "Content-Type":"application/json"}
        #gen_url = "http://%s/attendance/ruleAttendance?startDate=%s 00:00:00&endDate=%s 23:59:59"%(Requrl, yesterday, yesterday)
        gen_url = "http://%s/attendance/ruleAttendance?startDate=17-04-2019 00:00:00&endDate=17-04-2019 23:59:59"%(Requrl)
        print "Request attendance URL :: %s"%(gen_url)
        resp = requests.get(gen_url, headers=headers);
        print "attendance Response HTTP CODE :: %s"%resp
        if resp.text is not None:
            content = json.loads(resp.text)
        for key, value in content.items():
            processingDate = value['processingDate'].replace('-', '/') 
            attachments['totalMinutesWorked'] = value['totalMinutesWorked' ]
            attachments['documentName'] = value['documentName']
            attachments['objectType'] = value['objectType']
            attachments['processingDate'] = processingDate;
            req_url = "http://%s/rules/evalRules/LEAVE_RULES"%(Requrl) 
            resp = requests.post(req_url, headers=headers, data=json.dumps(attachments));
            print "Rules_responce_code", resp

    except Exception as er:
        print "Attendance Exception error:: %s"%er

if __name__ == "__main__":
    
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    params = {}
    params['host'] = "10.6.4.21"
    params['port'] = int("8080")
    params['userName'] = "Sifi"
    login(params)
    #scheduler.add_job(login, trigger='interval', minutes=1, kwargs={'job':params})

