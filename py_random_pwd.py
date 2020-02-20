import string
import random

def py_random_pwd():
    
    try:
        chars = string.ascii_letters + string.digits;
        #chars = string.digits;
        password = ''
        for i in range(8):
            password += random.choice(chars)
        print "Random Password ::",password
    except Exception as er:
        print "Exception Error %s"%er

    return password

py_random_pwd()
