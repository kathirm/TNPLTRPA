import requests
import json, os, sys


def payment_gateway():
    resp = None
    try:

        headers = {
                "Content-Type" : "application/json", 
                "MerchantId" : "889061f5-5deb-4593-b742-8ece89222bf6", 
                "MerchantKey" : "STXEDSMMRCLXBXOYWSUYYPOZGCJSFYAHYTZTPCET"
                }

        sample_data  = {
                 "MerchantOrderId":"2014111903",
                 "Customer":
                        {
                        "Name":"Buyer Credit Authentication",
                        "Identity":"12345678912",
                        "IdentityType":"cpf"
                        },
                 "Payment":
                        {
                            "Type":"CreditCard",
                            "Amount":0,
                            "Installments":1,
                            "Authenticate":"true",
                            "SoftDescriptor":"123456789ABCD",
                            "ReturnUrl":"https://www.cielo.com.br",
                       "CreditCard":
                            {
                             "CardNumber":"1234123412341234",
                             "Holder":"Teste Holder",
                             "ExpirationDate":"12/2030",
                             "SecurityCode":"123",
                             "Brand":"Visa"
                            },
                       "ExternalAuthentication":
                            {
                             "Cavv":"123456789",
                             "Xid":"987654321",
                             "Eci":"5"
                            }
                        }
                }

        url = "https://apisandbox.cieloecommerce.cielo.com.br/1/sales/"
        resp = requests.post(url, headers=headers, data = json.dumps(sample_data))

    except Exception as er:
        print("\n [WARNING] PAYMENT GATEWAY TESTING EXCEPTION :: %s"%er)

    return resp
