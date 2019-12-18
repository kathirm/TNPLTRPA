import psycopg2

try:
    conn = psycopg2.connect(database = "TERAFASTWORKS", user = "postgres", password = "abcd123", host = "10.6.7.88", port = "5432")
except:
    print("I am unable to connect to the database") 

cur = conn.cursor()


sqlGetTableList = "\dt"
cur.execute(sqlGetTableList)
tables = cur.fetchall()


try:
    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")    
except:

    print("I can't drop our test database!")
"""

def insert_vendor_list(vendor_list):
    conn = psycopg2.connect(database = "TERAFASTWORKS", user = "postgres", password = "abcd123", host = "10.6.7.85", port = "5432")
    cur = conn.cursor()
    #cur.execute("CREATE TABLE testquetest(customerName varchar, databaseName varchar, customerPwd varchar, productType varchar, totalAmount integer, CardNumber varchar, cardHolderName varchar, expiredMonth varchar, expiredYear integer, cardCVV integer, customerEmail varchar)")


    sql = "INSERT INTO testquetest (customerName, databaseName, customerPwd, productType, totalAmount, CardNumber, cardHolderName, expiredMonth, expiredYear, cardCVV, customerEmail) VALUES ('TerafastNetworks', 'TerafastNetworks', 'XXXXXX', 'XXX', '1200', '123454678910', 'TerafastAdmin', 'Aug', '2021', '333', 'terafastnetworks@terafastnet.com')"
#   sql = "INSERT INTO testquetest (customerName, databaseName, customerPwd, productType, totalAmount, CardNumber, cardHolderName, expiredMonth, expiredYear, cardCVV, customerEmail) VALUES ('TerafastNetworks', 'TerafastNetworks', 'XXXXXX', 'XXX', '1200', '123454678910', 'TerafastAdmin', 'Aug', '2021', '333', 'terafastnetworks@terafastnet.com')"
    
    try:
        cur.execute(sql)
        conn.commit()


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
if __name__ == '__main__':
        # insert one vendor
        #insert_vendor("3M Co.")
        # insert multiple vendors
        insert_vendor_list([
            ('AKM Semiconductor Inc.',),
            ('Asahi Glass Co Ltd.',),
            ('Daikin Industries Ltd.',),
            ('Dynacast International Inc.',),
            ('Foster Electric Co. Ltd.',),
            ('Murata Manufacturing Co. Ltd.',)
            ])

"""   
conn.commit() # <--- makes sure the change is shown in the database
    
conn.close()
    
cur.close()

