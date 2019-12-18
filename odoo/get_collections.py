# import the PostgreSQL adapter for Python

import psycopg2
# Connect to the PostgreSQL database server
postgresConnection = psycopg2.connect(database = "TERAFASTWORKS", user = "postgres", password = "abcd123", host = "10.6.7.85", port = "5432") 
# Get cursor object from the database connection
cursor                = postgresConnection.cursor()

name_Table            = "news_stories"

sqlGetTableList = "select table_name from information_schema.tables"
#sqlGetTableList = "\dt"
cursor.execute(sqlGetTableList)

tables = cursor.fetchall()

print tables

