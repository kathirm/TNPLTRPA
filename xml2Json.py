xmlData = "<CreateAccountResponse xmlns='https://iam.amazonaws.com/doc/2010-05-08/'><CreateAccountResult><Account><AccountId>100000130518</AccountId><CanonicalId>677A9E9A2ED8130665D70C07783A6487CF516749306DBC630701103B923EAEBC</CanonicalId><CreateDate>2020-03-17T12:44:59.540Z</CreateDate></Account></CreateAccountResult><ResponseMetadata><RequestId>b8f2b221b0a2e114ee3bda93746adae97c8f747ac5ab81ac</RequestId></ResponseMetadata></CreateAccountResponse>"

import xmltodict, json
xpars = xmltodict.parse(xmlData)
json = json.dumps(xpars)
print json
