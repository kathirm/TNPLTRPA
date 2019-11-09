
import json, sys,os, requests
from datetime import datetime, timedelta
import schedule, requests


def update():

    try:
        tntName = "Terafastnet"
        pwd = "!changeme!"
        headers = []
        login_url = "http://controller:8080/auth/login?username=Admin@%s&password=%s" %(tntName, pwd)
        token = requests.get(login_url, headers)
        if token.text is not None:
            token_dict= json.loads(token.text)
            if 'access-token' in token_dict:
                token = token_dict['access-token']
                print "retrived token for the user " + tntName + " with token: " + token

        headers = {"Authorization" : "Bearer %s"%token}
        getUrl  = "http://controller:8080/search?q=TYPE:%22Application%22"
        resp = requests.get(getUrl, headers=headers)
        getappData = json.loads(resp.text)
        
        flg = {}
        #flg["forceCheckout"] = False 
        flg["docStatus"] = "DRAFT"
       
        flg["shiftTime"] = "10.00"
        
        head = {"Authorization" : "Bearer %s"%token, "Content-Type":"application/json"}
        for data in getappData["Applications"]:
            Data =  data["replaceContent"]
            uIds =  Data.get("uId")
            _id = data.get("_id")
            genUr = "http://controller:8080/imports/%s"%_id
            resp = requests.patch(genUr, headers=head, data=json.dumps(flg))
            print resp, _id

    except Exception as er:
        print "Update Value function Exception :: %s"%er


update()
