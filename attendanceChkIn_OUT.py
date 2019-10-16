import datetime , json, sys, requests
from random import randrange

def date_backward(token, uId, chkType, inpttime):
    try:
        dtlist = [] #get_backward date
        tmlist = [] #get_time's Random
        headers = {"Authorization" : "Bearer %s"%token}
        cur = datetime.date.today()
        curdte = str(cur.strftime("%d-%m-%Y"))   
        datem = cur.strftime("%m-%Y")
        print "Today Date :: %s Current month & Year :: %s"%(curdte, datem)
        prvdte = str("01-"+"%s")%(datem)        

        curRange = cur.strftime("%d")
        dterange =  int(curRange)-1

        start = datetime.datetime.strptime(prvdte, "%d-%m-%Y")
        end = datetime.datetime.strptime(curdte, "%d-%m-%Y")
        date_array = (start +  datetime.timedelta(days=x) for x in range(0, (end-start).days))
        for date_object in date_array:
            dte = (date_object.strftime("%Y-%m-%d"))
            dtlist.append(dte)

        startDate = datetime.datetime(2013, 9, 20,inpttime,00)
        for x in time_generator(startDate, dterange):
            time =  x.strftime("%H:%M:00")
            tmlist.append(time)

        totalList = []
        for i in range(dterange):
            total = {}
            total["Date"] = dtlist[i]
            total["time"] = tmlist[i]
            totalList.append(total)

        for i in totalList:
            date = i.get("Date")
            time = i.get("time")
             
            genurl = "http://controller:8080/attendance?uId=%s&%s=%sT%s.948Z"%(uId, chkType, date, time)
            resp = requests.post(genurl, headers=headers)
            print "Response :: %s CheckType :: %s uId :: %s Date&time :: %s %s"%(resp, chkType, uId, date, time)
    except Exception as er:
        print "date generator Exception Error :: %s"%er

def time_generator(start, l):
    current = start
    while l >= 0:
        current = current + datetime.timedelta(minutes=randrange(10))
        yield current
        l-=1

#startDate = datetime.datetime(2013, 9, 20,10,00)
#for x in time_generator(startDate, 25):
#    print x.strftime("%H:%M")


def login(tenatName, uId, chkType, inpttime):
    try:
        token = None
        pwd = "!changeme!"
        login_url = "http://controller:8080/auth/login?username=Admin@%s&password=%s" %(tenatName, pwd)
        headers = []
        token = requests.get(login_url, headers)
        if token.text is not None:
            token_dict= json.loads(token.text)
            if 'access-token' in token_dict:
                token = token_dict['access-token']
                print "retrived token for the user " + tenatName + " with token: " + token
        date_backward(token, uId, chkType, inpttime)
    except Exception as er:
        print "Login Exception :: %s"%er

    return token


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print "Usage: %s <1.tenantName, 2.uId, 3.AttType, 4.InputTime>" % (sys.argv[0])
        sys.exit(0);

    tntName = sys.argv[1]
    uId = sys.argv[2]
    chkType = sys.argv[3]
    inpttime = int(sys.argv[4])
    token = login(tntName, uId, chkType, inpttime) 
