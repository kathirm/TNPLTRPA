
import json, sys,os, requests
from datetime import datetime, timedelta
import schedule, requests

if len(sys.argv) != 2:
    print("\n [WARNING] PLEASE INPUT ARGUMENT OF [-IP ADDRESS-] EX:'xxx.xx.xx.xxx'")
    sys.exit(0);
ip = sys.argv[1]


def update():

    try:
        tntName = "Pronto"
        pwd = "!changeme!"
        headers = []
        login_url = "http://%s:8080/auth/login?username=Admin@%s&password=%s" %(ip, tntName, pwd)
        print("\n [INFO] LOGIN URL : %s"%login_url)
        token = requests.get(login_url, headers)
        if token.text is not None:
            token_dict= json.loads(token.text)
            if 'access-token' in token_dict:
                token = token_dict['access-token']
                print "retrived token for the user " + tntName + " with token: " + token

        headers = {"Authorization" : "Bearer %s"%token}
        getUrl  = "http://%s:8080/search?q=TYPE:%22Application%22"%ip
        print("\n [INFO] GET APPLICATION LIST URL :: %s"%getUrl)
        resp = requests.get(getUrl, headers=headers)
        getappData = json.loads(resp.text)
        
        flg = {}

        #flg["forceCheckout"] = False 
        #flg["docStatus"] = "DRAFT"
       
        #flg["shiftTime"] = "10.00"
        
        head = {"Authorization" : "Bearer %s"%token, "Content-Type":"application/json"}
        for data in getappData["Applications"]:
            Data =  data["replaceContent"]
            uIds =  Data.get("uId")
            _id = data.get("_id")
            genUr = "http://%s:8080/imports/%s"%(ip, _id)
            print("\n {INFO] UPDATE PATCH CALL URL :: %s"%genUr)
            resp = requests.patch(genUr, headers=head, data=json.dumps(flg))
            print resp, _id

    except Exception as er:
        print "Update Value function Exception :: %s"%er


update()
