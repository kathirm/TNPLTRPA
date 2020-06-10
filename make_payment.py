import json, sys, os
import requests
import logging

class make_payment:

    def __init__(self, merchantId, merchantKey, url):

        logging.basicConfig(level=logging.DEBUG)
        self.merchantId  = merchantId;
        self.merchantKey = merchantKey;
        self.url = "https://"+url
        
    def payload_form(self, params=None):
        try:
            resp = None
            payload = {}
            credit_card = {}
            payment = {}
            payload["MerchantOrderId"] = params.get("merchantOrderId") 

            with open("/etc/payload.json") as f:
                record = json.load(f)
                for rows in record:
                    payload["Customer"] = rows.get("custInfo")
                    payment = rows.get("payment")
                    payment["Amount"] = params.get("totalAmount") 
                    payload["Payment"] = payment 

            expry_date = str(params.get("expiredMonth")) +'/'+ str(params.get("expiredYear"))
            credit_card["CardNumber"] = params.get("CardNumber")
            credit_card["Holder"] = params.get("cardHolderName")
            credit_card["ExpirationDate"] = expry_date
            credit_card["SecurityCode"] = params.get("cardCVV")            
            getCardDigit = params.get("CardNumber")[0]
            for typ in record:
                 cardType = typ[getCardDigit]
            credit_card["Brand"] = cardType.get("Type")

            payment["CreditCard"] = credit_card
            payload["Payment"] = payment

            resp = self.makePayment(payload)

        except Exception as er:
            logging.warning("[WARNING] PAYLOAD FORM EXCEPTION ERROR :: %s"%er)
        return resp

    def makePayment(self, payload_val):
        try:
            body = None
            headers = {
                    "Content-Type" : "application/json",
                    "MerchantId" : self.merchantId,
                    "MerchantKey" : self.merchantKey
                    }
            resp = requests.post(self.url, headers = headers, data=json.dumps(payload_val))
            if resp is None:
                pass;
            elif resp.status_code >= 400:
                body= resp.text
            elif resp.status_code >= 200 and resp.status_code < 300:
                returnResp = json.loads(resp.text)
                return_code = returnResp["Payment"]["ReturnCode"]

                body = {}
                body["PaymentId"] = returnResp["Payment"]["PaymentId"]
                body["Tid"] = returnResp["Payment"]["Tid"]
                body["cardNumber"] = returnResp["Payment"]["CreditCard"]["CardNumber"]
                body["ReceivedDate"] = returnResp["Payment"]["ReceivedDate"]
                if str(return_code) == "0":
                    body["ReturnCode"] = returnResp["Payment"]["ReturnCode"]
                    body["AuthenticationUrl"] = returnResp["Payment"]["AuthenticationUrl"]                  
                    body["ReturnUrl"] = returnResp["Payment"]["ReturnUrl"]
                else:

                    body["ReturnCode"] = returnResp["Payment"]["ReturnCode"]
                    body["ReturnMessage"] = returnResp["Payment"]["ReturnMessage"] 
            else:
                paymentId = {"Message": "Credit card payment some technical Issues"}
            logging.info("[INFO] PAYMENT GATEWAY INFO :: %s"%body)

        except Exception as er:
            logging.warning("[WARNING] MAKEPAYMENT GATEWAY EXCEPTION :: %s"%er)

        return body
