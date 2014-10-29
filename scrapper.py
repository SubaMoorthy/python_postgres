'''
Created on Oct 6, 2014
@author: Suba
'
'''

import psycopg2
from filterJSON import finalJSON, required_keys



HOSTNAME = 'localhost'
DBNAME = 'webscraping'
USER = 'postgres'
PASSWORD = 'postgres'
conn_string = "host=\'"+ HOSTNAME + "\' dbname=\'" + DBNAME +'\' user=\'' + USER + '\' password=\''+ PASSWORD + '\''
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
'creating the column names string to mention the columns to be data should be inserted into'
column_data = ''
'required array has the column names to be inserted '
for i in range (0 , len(required_keys)):
    column_data += '%(' + required_keys[i] + ')s'
    if i != len(required_keys)-1:
        column_data += ','

'insert from python list into postgres'
cursor.executemany(
"INSERT INTO players VALUES (" + column_data+ ")", finalJSON
)
conn.commit()

cursor.execute('select * from players')
rows = cursor.fetchall()
print ("\n PLAYER DATA FROM DB:\n")
for row in rows:
    print  ("\n", row)
