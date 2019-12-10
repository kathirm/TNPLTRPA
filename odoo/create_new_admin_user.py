
print('\n [INFO]Create new_external user in Admin Role')

import json
import xmlrpclib
import requests
import sys

portal_url = "http://10.6.7.85:8069"
portal_db = "terafast"
admin_username = "mravi@terafastnet.com"
admin_password = "abcd123"

def create_external_user(params):    
    try:
        user_id = None;
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(portal_url))
        admin_uid = common.authenticate(portal_db, admin_username, admin_password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(portal_url))

        client_username = params.get("client_username")
        client_name = params.get("client_name")
        client_password = params.get("client_password")

        user_id  = models.execute_kw(portal_db, admin_uid, admin_password, 'res.users', 'signup', [{
            'login': client_username,
            'name': client_name,
            'password': client_password,
        }])
        print('\n [INFO] CREATE NEW USERNAME IN ODOO COMPLETED:: %s'%user_id)

        if user_id is None:
            print("\n [WARNING] USERNAME or EMAIL ID IS ALREADY EXIST IN ODOO SERVER")

    except Exception as er:
            print("\n [WARNING] Create new user function Exception :: %s"%er)

    return user_id

if __name__ == "__main__":

    if len(sys.argv) !=4:
        print("\n [WARNING] Usage: %s 1. <Email-id>,  2.<username>, 3.<password> Required" % (sys.argv[0]))
        sys.exit(0);

    params = {}
    params['client_username'] = sys.argv[1]
    params['client_name'] = sys.argv[2]
    params['client_password'] =  sys.argv[3]
    print("\n [INFO] INPUT ARGUMENTS VALUE :: %s"%params)
    create_external_user(params)




