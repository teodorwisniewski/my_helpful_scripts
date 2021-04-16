import os
import pandas as pd
import psycopg2


# List of variables that have to be defined by users of this script.
hostname = os.environ.get('HOST_POSTGRES')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASS') #
database = os.environ.get('DATABASE_NAME_POSTGRES')
schema_name = 'schema_name'
table_name =  'table_name'


# Simple routine to run a query on a database and print the results:
def do_query(conn, table_name) :
    cur = conn.cursor()
    cur.execute( f"SELECT * FROM {table_name}" )
    query_output_df = display_as_table(cur.fetchall(), cur.description)
    return query_output_df


def display_as_table(data, headers):
    df = pd.DataFrame(data=data, columns=[i[0] for i in headers])
    return df


print( "Using psycopg2:" )

my_connection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
with my_connection as conn:
    df = do_query( my_connection, schema_name + '.' + table_name)
print(df.head())

