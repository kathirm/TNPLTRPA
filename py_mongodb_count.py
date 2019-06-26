import json, os, sys
from pymongo import MongoClient
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
#SMTP_SERVER
import os, smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



def py_mongodb_count(job): 
    try:
        dbList = []
        dbname = []
        count = []
        host  = job["host"]
        port = job["port"]
        url = 'mongodb://'+host + ':' + str(port) + '/'
        print "Connectiong Mongodb serverIP :: %s && port :: %s"%(host, port)
        client = MongoClient(url) 
        cursor = client.list_databases() #get mongodb listofCollecions 
        for dbName in cursor:
            dbNamaList = dbName["name"]
            dbList.append(dbNamaList) #append list of collectionNames
        for dblist in dbList:
            db = client[dblist]
            conn = db['ObjectRepos']
            getRecords = find_Records(dblist, conn) #get Collections ObjectRepos ApplicationCount
            dbname.append(dblist)
            count.append(getRecords)
            coldata = dict(zip(dbname, count)) #Zip into one dictionary formatJson
        write_file = write_into_json_file(coldata) #write to current Applications count in Jsonfile 
    except Exception as er:
        print "collect mongodb COllections Exception Error:: %s"%(er)

def find_Records(dbName, conn):
    try:
        getRecordsCount = conn.find({"objectType" : "Application"}).count() 
    except Exception as er:
        print "connect Mongodb to findNumber of Applications Exception Error:: %s"%er
    return getRecordsCount

def write_into_json_file(data):
    try:
        curdate = datetime.date.today()
        fileName = str(curdate) + '.json'
        with open(fileName, 'w') as fout: #write into current Date applications count in Jsonfile 
            json.dump(data, fout)
        read_file_to_compare_count(fileName) #move currentDate & Previous date comparetionCount
    except Exception as er:
        print "collection Count write into json file Exception er :: %s"%er

def read_file_to_compare_count(fileName):
    try:
        Dict_A = {} #currentDate_Count 
        Dict_B = {} #Yesterday_Count 
        output_Dict = {}#Application different_Count
        PreDate = datetime.datetime.today() - datetime.timedelta(days=1)
        Date = PreDate.strftime ('%Y-%m-%d') #get yesterday date
        Predatefile = str(Date) + '.json';
        with open(fileName) as f:
            data = json.load(f)
            Dict_A = data #store currentdate ApplicationsCount in Dict_A
        with open(Predatefile) as fout:
            preCount = json.load(fout)
            Dict_B = preCount #store Yesterday ApplicationCount in Dict_B

        for key in Dict_A.keys(): #check Dict_A keys
            if key in Dict_B.keys(): #compare keys into Dict_A && Dict_B are same
                output_Dict[key] = abs(Dict_A[key] - Dict_B[key]) #get difference between currentDate & previous dayCount
        print output_Dict
        eMailBody = open("/home/kathir/_py_programs_test/mdbcount.html",'w')
        html = """<html><head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td { padding: 7px;text-align: center;}</style></head><h4>Total Number of Applications COunt</h4><br></br><table border="1" width="50%"><tr><td>TenantName</td><td>Count</td>"""
        for data in output_Dict:
            html += "<tr>" 
            html += "<td>"+data+"</td>"
            html += "<td>"+str(output_Dict[data])+"</td>"
            html += "</tr>"
        targets = ['mkathir@terafastnet.com']
        #eMailBody = open("/home/kathir/_py_programs_test/mdbcount.html").read().format(output_Dict = json.dumps(output_Dict))
        send_Email(targets, subject = "mongoDb application count", body =html) 

        
    except Exception as er:
        raise er
        print "Read currentCount json & Previous CountJson file Exception Error :: %s"%er

def send_Email(targets, subject=None, body=None,attachment_file_path=None):
    try:
        smtp_ssl_host = "smtp.gmail.com"
        smtp_ssl_port = int(465);
        username = "terafastnet@gmail.com"
        password = "!terafast!"
        sender = "terafastnet@gmail.com"
        msg = MIMEMultipart()
        msg['To'] = ', '.join(targets);
        if subject is not None:
            msg['Subject'] = subject;
        if body is not None:
            txt = MIMEText(body, 'html')
            msg.attach(txt)
        if attachment_file_path is not None:
            filepath = attachment_file_path;
            with open(filepath, 'rb') as f:
                docx = MIMEApplication(f.read())
            docx.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
            msg.attach(docx)
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, password)
        server.sendmail(sender, targets, msg.as_string())
        server.quit()
        print "Mail Send Successfully %s"%(targets)
    except Exception as er:
        print "mailsend server Exception error:: %s"%er



if __name__ == "__main__":

    host = sys.argv[1];
    port = int(sys.argv[2]);
   
    scheduler = BackgroundScheduler()
    scheduler.start()
    print "Start the background  scheduler..."
    params = {}
    params['host'] = host
    params['port'] = port
    #py_mongodb_count(params)
    scheduler.add_job(py_mongodb_count, trigger='interval', seconds=1, kwargs={'job':params})



