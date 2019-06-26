import json, sys, os
import requests, time


class Pydocgen:

    def __init__(self, ctrlIP, ctrlPort,  userName):
        
        self.url = "%s:%s"%(ctrlIP, ctrlPort);
        self.userName = 'Admin@%s'%userName;
        self.password = "!changeme!"; 
        self.token = None;
        self.login()

    def login(self):
        #print 'userlogin credentials userName :: %s & Password :: %s'%(self.userName, self.password);
        try:
            print 'userlogin credentials userName :: %s & Password :: %s'%(self.userName, self.password);
            login_url = "http://" + self.url + "/auth/login?username=%s&password=%s" %(self.userName, self.password)
            headers = []
            self.token = requests.get(login_url, headers)
            if self.token.text is not None:
                token_dict= json.loads(self.token.text)
                if 'access-token' in token_dict:
                    self.token = token_dict['access-token']
                    print "retrived token for the user " + self.userName + " with token: " + self.token
        except Exception as err:
            print "error :", err
        return self.token;

    def gendec(self, body):
        try:
            url = "http://" + self.url + "/TeraRpa/applicationInfo";
            headers = {"Authorization" : "Bearer %s " %self.token, "Content-Type":"application/json"}
            inputJson = body
            i = 0 #init while value
            while i<1:
                i += 1; #+1 value in increase equalto tenNumbers
                ts = int(time.time()) #get_timestamp_value
                applicantName = inputJson["applicantName"]
                for key, value in inputJson.items():
                    if key == "applicantName": #if exist keyof inputjson value 
                        inputJson[key] = applicantName + str(i) + str(ts) #generateNew applicantName
                result = requests.post(url, headers=headers, data=json.dumps(inputJson), verify=False);
                print "generate application status :: %s"%result
                if result is None :
                    pass;
                elif result.status_code >= 400:
                    print "ApplicantName same " +str(result.status_code)
                elif result.status_code >= 200 and result.status_code < 300:
                    print "generate documentation Success.." +str(result.status_code)
                else:
                    print "invalid_status", result.status_code
            """
            #http://10.6.4.21:8080/TeraRpa/applicationInfo
            url = "http://" + self.url + "/TeraRpa/applicationInfo";
            headers = {"Authorization" : "Bearer %s " %self.token, "Content-Type":"application/json"}
            result = requests.post(url, headers=headers, data=json.dumps(my_dict), verify=False);
            print "generate application status :: %s"%result
            if result is None : 
                pass;
            elif result.status_code >= 400:
                print "ApplicantName same " +str(result.status_code)
            elif result.status_code >= 200 and result.status_code < 300:
                print "generate documentation Success.." +str(result.status_code)
            else:
                print "invalid_status", result.status_code
            """
        except Exception as er:
            print er

if __name__ == "__main__":


    ctrlIP = sys.argv[1];
    ctrlPort = int("8080"); 
    userName  = sys.argv[2];
    jsonFile = sys.argv[3];

    with open(jsonFile) as f:
        data = json.load(f)
        #data = json.load(f)
    login = Pydocgen(ctrlIP, ctrlPort, userName);
    login.gendec(data)
