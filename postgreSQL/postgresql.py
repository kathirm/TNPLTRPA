import psycopg2
from passlib.context import CryptContext


conn = psycopg2.connect(database="terafast", user = "postgres", password = "abcd123", host = "206.189.156.106", port = "5432")

print "Opened database successfully"


cur = conn.cursor()
cur.execute("SELECT * FROM res_users ")
rows = cur.fetchall()


for row in rows:
    print'\n [INFO] GET USER  ID:',row[0]
"""
newpass_crypt = CryptContext(['pbkdf2_sha512']).encrypt("newpass")
cur.execute("UPDATE res_users SET password = '"+newpass_crypt+"' WHERE id=69")
conn.commit()
conn.close()
print("Password for  has been updated successfully")
"""

#for row in rows:
#    print row



