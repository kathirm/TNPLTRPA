import psycopg2
from passlib.context import CryptContext

#conn = psycopg2.connect(database="postgres_db", user = "sysadmin", password = "abcd123", host = "127.0.0.1", port = "5432")
conn= psycopg2.connect(user = "postgres",
                                  password = "abcd123",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "terafast")
print("Opened database successfully")
cur = conn.cursor()


cur.execute("SELECT * FROM res_users ")

rows = cur.fetchall()
for row in rows:
   print('\n [INFO] GET USER  ID:',row)
