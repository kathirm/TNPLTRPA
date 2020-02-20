import xlrd, os, sys
import requests, json
import string
import random, xlsxwriter
from pandas import DataFrame

tenantName = sys.argv[1]
token = None
def login():
    tenant_Name = tenantName
    pwd = "!changeme!"
    login_url = "http://maher.terafastnet.com:8080/auth/login?username=Admin@%s&password=%s" %(tenantName, pwd)
    headers = []
    token = requests.get(login_url, headers)
    if token.text is not None:
        token_dict= json.loads(token.text)
        if 'access-token' in token_dict:
            token = token_dict['access-token']
            print "retrived token for the user " + tenantName + " with token: " + token

    return token

path = os.getcwd()
workbook = xlrd.open_workbook(path+"/"+"StudNameList.xlsx","rb")
sheet = workbook.sheet_by_index(0)
rows = []

username = []
studentpawd = []
studNameList = []

token = login()

for i in range(sheet.nrows):
    columns = []
    for j in range(sheet.ncols):
        columns.append(sheet.cell(i, j).value)
        rows.append(columns)
    studId =  int(columns[1])
    studName = str(columns[2])
    studMob = columns[3]

    chars = string.ascii_letters + string.digits;
    password = ''

    for i in range(8):
        credentials = []
        password += random.choice(chars)

    user_name = str(studId) +"@"+tenantName
    randomPwd =  password

    username.append(user_name)
    studentpawd.append(randomPwd)
    studNameList.append(studName)

#df = DataFrame({'2. User Name': username, '3. Password':studentpawd, '1. Student Name':studNameList })
#df.to_excel(path + '/'+'MaherLoginList.xlsx', sheet_name='sheet1', index=False)

    kwargs = {
        "username" : user_name,
        "password" : randomPwd,
        "tenant" : tenantName,
        "role" : "Student",
        "emailUsername" : "Students@terafastnet.com",
        "userStatus" : "Active",
        "statusReason" : "",
        "blockCheckout" : "false",
        "authTypes" : [
            "password"
            ]
        }
    url = "http://maher.terafastnet.com:8080/users"
    headers = {"Authorization" : "Bearer %s"%token, "Content-Type":"application/json"}
    resp = requests.post(url, headers = headers , data = json.dumps(kwargs))
    if resp.status_code >= 200 and resp.status_code < 300:
        print("[INFO] NEW USER CREATED SUCCESSFULL HTTP RESPONSE CODE : %s"%resp)
    elif resp.status_code >= 400:
        print("[WARNING] NEW USER CREATED RESPONSE FAILED")
    else:
        print("[WARNING] INVALID RESPONSE CODE")

df = DataFrame({'2. User Name': username, '3. Password':studentpawd, '1. Student Name':studNameList })
df.to_excel(path + '/'+'MaherLoginList.xlsx', sheet_name='sheet1', index=False)
