import json, os, sys
import datetime as dt
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
        param_map = {
                "totalMinutesWorked": 0,
                "documentName": "pbala_004.docx",
                "processingDate": "09/07/2019",
                "objectType": "Application"
                }
        headers = {"Authorization" : "Bearer %s " %token, "Content-Type":"application/json"}
        gen_url = 'http://'+Requrl + '/rules/evalRules/LEAVE_RULES'
        resp = requests.post(gen_url, headers=headers, data = json.dumps(param_map));
        print resp.text

    except Exception as er:
        print "Attendance Exception error:: %s"%er

if __name__ == "__main__":

    params = {}
    params['host'] = "10.6.4.21"
    params['port'] = int("8080")
    params['userName'] = "Terafast"
    login(params)


