import json
import xmlrpclib

username = 'admin'
pwd = 'admin'     
dbname = 'Tester3'

sock_common = xmlrpclib.ServerProxy ('http://206.189.156.106:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
print uid
sock = xmlrpclib.ServerProxy('http://206.189.156.106:8069/xmlrpc/object')

partner = {
        'name': 'Administrator',
        'lang': 'pt_BR'
        }
partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner)














