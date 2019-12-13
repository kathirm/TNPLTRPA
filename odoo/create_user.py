import json
import xmlrpclib
import requests
import psycopg2
from passlib.context import CryptContext


portal_url = "http://10.6.7.85:8069"
portal_db = "terafast1" 
admin_username = "admin"
admin_password = "abcd123"

def connect_sqldb():
    try:
        conn = psycopg2.connect(database="terafast1", user = "postgres", password = "abcd123", host = "10.6.7.85", port = "5432")
        cur  = conn.cursor()
    except Exception as e:
        print("\n [WARNING] CONNECT POSTGRESQL DATABASE CONNECTION ERROR ::%s"%e)
    
    return conn 

def reset_pwd(user_id):
    try:
       conn = connect_sqldb()
       cur = conn.cursor()
       newpass_crypt = CryptContext(['pbkdf2_sha512']).encrypt("abcd123")
       cur.execute("UPDATE res_users SET password = '"+newpass_crypt+"' WHERE id=%s"%(user_id))
       conn.commit()
       conn.close()
       print("\n [INFO] PASSWORD FOR USERID :: %s HAS BEEN UPDATED SUCCESSFULLY"%user_id)

    except Exception as er:
        print("\n [WARNING] CREATED USERID :: %s  PASSWORD RESET FUNCTION ERROR ::%s"%(user_id, er))


def create_internal_new_user(params):
    
    try:    
        user_id = None;
        client_username = params.get('client_name')
        client_name = params.get('client_username')
        client_password = params.get('client_password')

        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(portal_url))
        uid = common.authenticate(portal_db, admin_username, admin_password, {}) 
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(portal_url))

        user_id = models.execute_kw(portal_db, uid, admin_password, 'res.users', 'create', [{
            'name': client_username, 
            'login':client_name,
            'company_ids':[1],
            'company_id':1, 
            'new_password': client_password,

        }])
        print('\n [INFO] CREATE NEW USERNAME IN ODOO COMPLETED:: %s'%user_id)

        if user_id is None:
            print("\n [WARNING] USERNAME or EMAIL ID IS ALREADY EXIST IN ODOO SERVER")
        else:
            reset_pwd(user_id)

    except Exception as er:
            print('\n [WARNING] CREATE NEW INTERNAL USER FUNCTION EXCEPTION ERROR :: %s'%er)

    return user_id


if __name__ == "__main__":
    import sys
    if len(sys.argv) !=4 :
        print("\n [WARNING] usage : %s 1. Email-id, 2. username, 3. password"% (sys.argv[0]))
        sys.exit(0);

    params = {}
    params['client_username'] = sys.argv[1];
    params['client_name'] = sys.argv[2];
    params['client_password'] = sys.argv[3];

    print("\n [INFO] INPUT ARGUMENTS VALUE :: %s"%params)
    create_internal_new_user(params)
