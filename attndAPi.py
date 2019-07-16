import json, os, sys
from flask import Flask, flash, request, redirect, url_for
import requests
from flask import jsonify

app = Flask(__name__)
app.config['DEBUG'] = True

#Configuration_login
UserName = "Terafast"
Pwd = "!changeme!"

@app.route("/")
def index():
    return ("Terafast RFID Test")

#@app.route("/login")
def login():
    try:
        token = None;
        login_url = "http://controller:8080/auth/login?username=Admin@"+UserName+"&password="+Pwd
        headers = []
        token = requests.get(login_url, headers)
        if token.text is not None:
            token_dict= json.loads(token.text)
            if 'access-token' in token_dict:
                token = token_dict['access-token']
    except Exception as er:
        raise er 

    return token

@app.route("/attendance/status/<startdate>/<enddate>")
def emp_status_report(startdate=None, enddate=None):
    try:
        token = login()
        headers = {"Authorization" : "Bearer %s " %token, "Content-Type":"application/json"}
        getstatus = "http://controller:8080/attendance/status?startDate="+startdate+" 00:00:00&endDate="+enddate+" 23:59:59"
        resp = requests.get(getstatus, headers = headers)

    except Exception as er:
        raise er

    return jsonify({"status" : resp.text})

@app.route("/attendance/detailed/<startdate>/<enddate>/<uId>")
def emp_detailed_report(startdate, enddate, uId):
    try:
        token = login()
        headers = {"Authorization" : "Bearer %s " %token, "Content-Type":"application/json"}
        empDetails = "http://controller:8080/attendance/detailed?startDate=%s 00:00:00&endDate=%s 23:59:59&uId=%s"%(startdate, 
                enddate, uId)
        resp = requests.get(empDetails, headers = headers)

    except Exception as er:
        raise er

    return jsonify({"detailedReport" :resp.text})


@app.route("/attendance/summary/<startdate>/<enddate>")
def emp_summary_report(startdate, enddate):
    try:
        token = login()
        headers = {"Authorization" : "Bearer %s " %token, "Content-Type":"application/json"}
        getSummary = "http://controller:8080/attendance/summary?startDate="+startdate+" 00:00:00&endDate="+enddate+" 23:59:59"
        resp = requests.get(getSummary, headers = headers)

    except Exception as er:
        raise er

    return jsonify({"getSummary" : resp.text})



if __name__ == "__main__":

    app.run(host='10.6.7.88', port = 9000)
