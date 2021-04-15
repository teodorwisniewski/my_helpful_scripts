import os

hostname = 'localhost'
username = 'postgres' #os.environ.get('DB_USER')
password = os.environ.get('DB_PASS_LOCAL') #
database = 'analysis'

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT * FROM example LIMIT 5" )

    for row in cur.fetchall() :
        print( row )


print( "Using psycopg2:" )
import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()

