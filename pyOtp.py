import pyotp, sys


getBase64 = sys.argv[1]
totp = pyotp.TOTP(getBase64)

print "Currents SHA_285 Code :: %s"%totp.now()









