import psycopg2
from credentials import DB_STR

conn = psycopg2.connect(DB_STR)
cursor = conn.cursor()


query_insert = '''INSERT INTO Author (first_name, last_name, password) select %s, %s, %s;'''
cursor.execute(query_insert, ('John', 'Down','qwerty123')) # send data to current session(locally)
conn.commit() # write data to db


query_select = '''
select * FROM author;
'''

cursor.execute(query_select) # execute read query

rows = cursor.fetchall() # write to value

for item in rows:
    print (item)