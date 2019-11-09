import sys, time
import csv, json
from zk import ZK
from datetime import datetime
import requests

def login():
    try:
        userName  = "Terafast"
        Password  = "!changeme!"
        token = None;
        login_url = "http://controller:8080/auth/login?username=Admin@%s&password=%s" %(userName, Password)
        headers = []
        token = requests.get(login_url, headers)
        if token.text is not None:
            token_dict= json.loads(token.text)
            if 'access-token' in token_dict:
                token = token_dict['access-token']
                print "retrived token for the user " + userName + " with token: " + token
        headers = {"Authorization" : "Bearer %s " %token, "Content-Type":"application/json"}
    except Exception as er:
        print "Controller get access-token login in exception : %s"%er

    return headers

def daily_attendance(data=None, headers=None):
    try:
        today = datetime.today()
        d1 = today.strftime("%d-%m-%Y")
        print "Today",d1 

        with open("schdata.json", "r") as Fint:
            schdata = json.load(Fint)
            flen = len(schdata)
            print flen

        if flen == 0:
            if data is not None:
                with open("schdata.json", "w") as intf:
                    intf.write(data)
            else:
                print "No data found"
        else:
            ids = []
            listofTime = []
            for i in schdata:                
                getdate = i.get("Date")
                getuId  = int(i.get("uId"))
                empName = i.get("Name")
                time = i.get("time")
                d_in_ms = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')
                if d1 == i["Date"] :#and getuId == 119:
                    print i["time"], i["uId"], i["Name"]                   
                    tdydict = {}
                    tdydict["Time"] = i["time"];
                    tdydict["uId"] = int(i["uId"]);
                    tdydict["Name"] = i["Name"]
                    tdydict[d1] = "IN"
                    listofTime.append(tdydict)

                    ids.append(int(i["uId"]))


            #print listofTime
            """
            with open('data.json', 'r+') as infh:
                data = json.load(infh)
                for i in  data:
                    if i[d1] == "IN" and i["uId"] == 119:
                        i[d1] = "OUT"
                        infh.seek(0)
                        json.dump(data, infh)
                        infh.truncate()
                        chkType = "OUT"
                        break
                    else:
                        if i[d1] == "OUT" and i["uId"] == 119:
                            i[d1] = "IN"
                            infh.seek(0)
                            json.dump(data, infh)
                            infh.truncate()
                            chkType = "IN"
                            break

            print "CHkTYPE", chkType

            with open("data.json", 'w') as infg:
                infg.write(json.dumps(listofTime))         

           
            myList = list(dict.fromkeys(ids))
            print myList
            for li in listofTime:
                for i in myList:
                    if i == li["uId"]:
                        return ids
                        print li.get("Name"), li.get("Time")
                         
            """
            #print listofTime
            #Newlogic
          
            """ 

            odddata = []
            evendata = []

            getcount = len(listofTime)
            for num in range(getcount):
                i = num+1;
                if i % 2 == 0:
                    evendata.append(listofTime[num])
                    for i in evendata:
                        uId = i["uId"]
                        d_ms = i.get("Time")
                        d_in_ms = datetime.strptime(d_ms, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')
                    #resp = upload_attendance("OUT", headers, uId, d_in_ms)
                else:
                    odddata.append(listofTime[num])
                    for j in odddata:
                        uId  = j.get("uId")
                        d_ms = j.get("Time")
                        d_in_ms = datetime.strptime(d_ms, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')                 
                    #resp = upload_attendance("IN", headers, uId, d_in_ms)


            print "ODD %s"%(odddata)
            print "EVEN %s"%(evendata)
            """
    except Exception as e:
        print "writeJson file exception er %s"%e

    return listofTime


def upload_attendance(chkType, headers, uId, d_in_ms):
    try:
        if chkType == "IN":
            gen_url = "http://controller:8080/attendance?uId=%s&checkin=%s"%(uId, d_in_ms)
            resp = requests.post(gen_url, headers=headers);
            print "check-IN daily attendance Post Respcode :: %s"%resp
        else:
            gen_url = "http://controller:8080/attendance?uId=%s&checkout=%s"%(uId, d_in_ms)
            resp = requests.post(gen_url, headers=headers);
            print "Check-OUT daily attendance Post Respcode :: %s"%resp

    except Exception as er:
        print "Controller via upload Attendance exception as :: %s"%er

    return resp


if __name__== '__main__':

    users = []
    ip = "10.6.8.3"#sys.argv[1]
    port = int(4370)#(sys.argv[2])

    zk = ZK(ip, port, force_udp=True, verbose=False);
    conn = zk.connect();

    users = conn.get_users();
    users_map = {}
    for user in users:
        if user.uid == 17:
            pass
        users_map[user.uid] = user;

    att_data = conn.get_attendance();

    exnd_dict = {}
    attend_list = []
    headers =  login()

    for data in att_data:
        uid = int(data.uid)
        if int(data.uid) in users_map.keys():
            attnd_dat = {}
            #print "User %s(%s,%s) punched at %s, %s, %s " %(users_map[uid].name, str(uid), str(users_map[uid].card), 
            #str(data.timestamp), str(data.punch), str(data.status))
            attnd_dat["Name"] = users_map[uid].name;
            attnd_dat["uId"]  = str(uid);
            attnd_dat["cardNum"] = str(users_map[uid].card);
            attnd_dat["time"] = str(data.timestamp);
            getdat = str(data.timestamp)
            date = datetime.strptime(getdat, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
            attnd_dat["Date"] = date; 
            attend_list.append(attnd_dat) 
        else:
            print "unknown user with  uid=%s punched at %s" %(uid, str(data.timestamp))    
        #attnd_json(attnd_dat, headers)
    #print json.dumps(attend_list)
    dicval = json.dumps(attend_list)
    with open("schdata.json", "w") as intf:
        intf.write(dicval)
    daily_attendance(dicval, headers)
    zk.disconnect()
       
