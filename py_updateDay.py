import json, os, sys
from datetime import datetime, timedelta
import schedule, requests

def login():
    try:
        tntName = "Pronto"
        pwd = "!changeme!"
        headers = []
        login_url = "http://139.59.18.236:8080/auth/login?username=Admin@%s&password=%s" %(tntName, pwd)
        token = requests.get(login_url, headers)
        if token.text is not None:
            token_dict= json.loads(token.text)
            if 'access-token' in token_dict:
                token = token_dict['access-token']
                print "retrived token for the user " + tntName + " with token: " + token

        getattendance(token)

    except Exception as er:
        print "login Exception error :: %s"%er

def getattendance(token):
    try:
        today = datetime.strftime(datetime.now() - timedelta(0), '%d-%m-%Y')
        current_month_text = datetime.now().strftime('%B')
        currentYear = datetime.now().year
        getYear = str(current_month_text) + '_'+ str(currentYear)

        headers = {"Authorization" : "Bearer %s"%token}
        genURl = "http://139.59.18.236:8080/attendance/getAttendance?checkin=%s 00:00:00&checkout=%s 23:59:59"%(str(today), str(today))
        resp = requests.get(genURl, headers = headers)
        data =  json.loads(resp.text)

        _chkIn = data.get("checkinList") 

        chkIn = []
        for usr in _chkIn:
            _iNid =  usr.get("uId")
            chkIn.append(_iNid)
        dif =  list(dict.fromkeys(chkIn))
        if dif is None:
            print "Today No Attendance Reords Found"

        getUrl  = "http://139.59.18.236:8080/search?q=TYPE:%22Application%22"
        resp = requests.get(getUrl, headers=headers)
        getappData = json.loads(resp.text)
        url = "http://controller:8080"
        Head = {"Authorization" : "Bearer %s " %token, "Content-Type":"application/json"}
        for data in getappData["Applications"]:
            Data =  data["replaceContent"]
            uIds =  Data.get("uId")
            if uIds in dif:
                #print data.get("name"), data.get("_id")
                atndData =  Data.get("attendanceDetails")               
                if atndData is None:
                    print "ValueNone"
                else:          
                    val = atndData
                    preWD = val.get(getYear)
                    iD =  data.get("_id")
                    if preWD is None:
                        body = {"attendanceDetails" : { getYear : 1}} 
                        genUrl  = url +'/imports/%s'%iD
                        resp = requests.patch(genUrl, headers =Head, data =json.dumps(body))
                        print resp
                    else: 
                        incseval = preWD + 1
                        body = {"attendanceDetails" : { getYear : incseval}}
                        genUrl  = url +'/imports/%s'%iD
                        resp = requests.patch(genUrl, headers =Head, data =json.dumps(body))
                        print resp

    except Exception as er:
        print "GetAttendance Exception error :: %s"%er



if __name__ == "__main__":
    login()
