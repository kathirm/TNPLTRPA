from flask import Flask
import payment
from flask import jsonify
from flask import Flask,redirect


import json
app = Flask(__name__)


@app.route('/')
def payment_gateway():

    resp = payment.payment_gateway()
    return_data =  resp.text
    
    return_url = json.loads(return_data)
    #url =  return_url["Payment"]["ReturnUrl"]
    url = "http://10.6.7.85:8008/payment_resp"
    
    return redirect(url, code=302)


if __name__ == '__main__':

    app.run(host='10.6.7.88', port=9000)
