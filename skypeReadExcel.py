import xlrd, os
from collections import OrderedDict
import simplejson as json
from datetime import datetime
from skpy import Skype #import skype messangerModule
from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.schedulers.blocking import BlockingScheduler
import schedule
import time 

def readDataFromExcelSheet():
    try:
        get_path = os.getcwd()
        wb = xlrd.open_workbook(get_path +'/TestExcel.xlsx')
        sh = wb.sheet_by_index(0)
        ##TDO appendData into data\_list variable
        data_list = []
        for rownum in range(1, sh.nrows):
            kwars = OrderedDict()
            row_values = sh.row_values(rownum)
            kwars['Name'] = row_values[0]
            excel_date = int(row_values[1])
            dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date - 2)
            kwars['Dob'] = str(dt)
            kwars['skypeId'] = row_values[2]
            ##TODO Append data into list
            data_list.append(kwars)

        data = json.dumps(data_list)
        #print data
        current_date = datetime.today().strftime('%m-%d')
        ##TODO Run throw the data in loop structure
        for i in json.loads(data):
            dob = str(i.get("Dob"))
            dob = dob[slice(5,10)]
            if dob == current_date:
                current_Name = i.get("Name")
                current_Dob  = i.get("Dob")
                current_skpId= i.get("skypeId")
                sendMsgToskYpe(current_Name, current_skpId)
                print"Name: %s, DateofBirth : %s, skypeId : %s"%(current_Name, current_Dob, current_skpId)

    except Exception as er:
        print("[WARNING] READ DATA FROM EXCEL SHEET EXCEPTION ERROR :: %s"%er)

def sendMsgToskYpe(empName, skypeId):
    try:
        sk = Skype("terafastnetworkteam@gmail.com", "Terafastnetworkspvtltd") # connect to Skype
        sk.user 
        cont = sk.contacts 
        sk.chats 
        ch = sk.contacts[skypeId].chat 
        ch.sendMsg("Hi %s (cake) On your special day, I wish you good luck. I hope this wonderful day will fill up your heart with joy and blessings. Have a fantastic birthday, celebrate the happiness on every day of your life. Happy Birthday!! (sparkler) (flower) "%empName)
        ch.getMsgs() 
    except Exception as er:
        print("[WARNING] SEND MESSAGE TO SKYPE EXCEPTION ERROR :: %s "%er)

scheduler = BackgroundScheduler()
scheduler.start()
job = scheduler.add_job(readDataFromExcelSheet, 'cron', hour='12', minute='25', second='00')
print"Current job starting....."
while True:
    time.sleep(45)

readDataFromExcelSheet()
