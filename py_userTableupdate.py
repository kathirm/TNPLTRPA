import json, sys, os
import requests


def login():
    try:
        token = None
        tenantName = sys.argv[1]
        pwd = "!changeme!"
        login_url = "http://controller:8080/auth/login?username=Admin@%s&password=%s" %(tenantName, pwd)
        headers = []
        token = requests.get(login_url, headers)
        if token.text is not None:
            token_dict= json.loads(token.text)
            if 'access-token' in token_dict:
                token = token_dict['access-token']
                print "retrived token for the user " + tenantName + " with token: " + token

        getusers(token, tenantName)
    except Exception as er:
        print "login Exception error :: %s"%er

    return token

def getusers(token, tenantName):
    try:
        headers = {"Authorization" : "Bearer %s"%token, "Content-Type":"application/json"}
        genURl = "http://controller:8080/users?&role=Employee"
        resp = requests.get(genURl, headers = headers)
        data = json.loads(resp.text)

        usr_dict = {}
        for usr in data: 
            _id =  usr.get("id")
            usr_dict["authTypes"] = ["blocked"]
            usr_dict["blockCheckout"] = "true"
            usr_dict["password"] = "blocked"
            genUr = "http://controller:8080/users/%s"%_id
            resp = requests.patch(genUr, headers=headers, data=json.dumps(usr_dict))
            print resp.text
            if resp.status_code >= 200 and resp.status_code < 300:
                print "User New Fields Updated Successfull Resp :: %s"%resp
            elif resp.status_code >= 400:
                print "User New Fields Updated Failed"
            else:
                print "Invalid Response COde"



    except Exception as er:
        print "getUsers Exception as error :: %s"%er

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Input params Missing<tenatName> failed"
        print "Usage: %s <tenantName>" % (sys.argv[0])
        sys.exit(0);
    login()
