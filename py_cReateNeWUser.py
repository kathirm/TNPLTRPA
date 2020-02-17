import json, sys, os
import requests

def login():
    try:
        token = None
        tenantName = sys.argv[1]
        pwd = "!changeme!"
        login_url = "http://159.65.157.226:8080/auth/login?username=Admin@%s&password=%s" %(tenantName, pwd)
        headers = []
        token = requests.get(login_url, headers)
        if token.text is not None:
            token_dict= json.loads(token.text)
            if 'access-token' in token_dict:
                token = token_dict['access-token']
                print "retrived token for the user " + tenantName + " with token: " + token
        cReatenewUser(token)
    except Exception as er:
        print "login Exception error :: %s"%er
    return token


def cReatenewUser(token):
    try:
        sampleData = {
                    "username" : "kavin@Terafastnet",
                    "password" : "!abcd123!",
                    "tenant" : "Terafastnet",
                    "role" : "Employee",
                    "emailUsername" : "Kavin@terafastnet.com", 
                    "userStatus" : "Active",
                    "statusReason" : "",
                    "blockCheckout" : "false",
                    "authTypes" : [ 
                        "password"
                        ]
                    }
        url = "http://159.65.157.226:8080/users"
        headers = {"Authorization" : "Bearer %s"%token, "Content-Type":"application/json"}
        resp = requests.post(url, headers = headers , data = json.dumps(sampleData))
        if resp.status_code >= 200 and resp.status_code < 300:
            print("[INFO] NEW USER CREATED SUCCESSFULL HTTP RESPONSE CODE : %s"%resp)
        elif resp.status_code >= 400:
            print("[WARNING] NEW USER CREATED RESPONSE FAILED")
        else:
            print("[WARNING] INVALID RESPONSE CODE")
    except Exception as er:
        print("[WARNING] CREATE NEW USER'S FUNCTION EXCEPTION :: %s"%er)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Input params Missing<tenatName> failed"
        print "Usage: %s <tenantName>" % (sys.argv[0])
        sys.exit(0);
    login()
