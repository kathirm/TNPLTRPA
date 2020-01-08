import pycurl
crl = pycurl.Curl()
crl.setopt(crl.URL, 'https://www.code-learner.com/post/')

data = '{"person":{"name":"billy", "email":"billy@example.com"}}'
buffer = BytesIO(data.encode('utf-8'))

crl.setopt(crl.UPLOAD ,1)
crl.setopt(crl.READDATA, buffer)

crl.perform()
crl.close()
