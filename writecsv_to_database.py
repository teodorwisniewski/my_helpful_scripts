

import psycopg2
import csv
import os


csv_file_name = 'csv_file_name.csv'
hostname = os.environ.get('HOST_POSTGRES')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASS') #
database = os.environ.get('DATABASE_NAME_POSTGRES')
schema_name = 'schema_name'
table_name =  'table_name'

conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
cur = conn.cursor()

with open(csv_file_name, 'r') as file:
    next(file) # skip csv header (first row with column titles)
    reader = csv.reader(file)
    for row in reader:
        # insert row here
        cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s);", row)
conn.commit()
conn.close()