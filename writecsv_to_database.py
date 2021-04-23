

# external imports
import psycopg2
import csv
import os

#internal imports
from creating_sql_query_table_from_csv import turn_csv_into_sql_table
from load_data_to_pandas_from_postgres_database import read_sql_table_to_df


csv_file_name = 'world_happiness_report.csv'
hostname = os.environ.get('HOST_POSTGRES')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASS') #
database = os.environ.get('DATABASE_NAME_POSTGRES')
schema_name = 'public'
table_name = 'world_happiness_report'

conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )


with conn as conn:
    cur = conn.cursor()
    create_table_sql_query = turn_csv_into_sql_table(csv_file_name, schema_name, table_name, save_to_file=False)
    for query in create_table_sql_query:
        cur.execute(query)

df = read_sql_table_to_df(conn, schema_name, table_name)
print(df.head())

# with open(csv_file_name, 'r') as file:
#     next(file) # skip csv header (first row with column titles)
#     reader = csv.reader(file)
#     for row in reader:
#         # insert row here
#         cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s);", row)
# conn.commit()
# conn.close()