

# external imports
import psycopg2
import csv
import os
import pandas as pd
import numpy as np

#internal imports
from creating_sql_query_table_from_csv import turn_csv_into_sql_table
from load_data_to_pandas_from_postgres_database import read_sql_table_to_df


csv_file_name = 'updated_sample_submission.csv'
hostname = os.environ.get('HOST_POSTGRES')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASS') #
database = os.environ.get('DATABASE_NAME_POSTGRES')
schema_name = 'public'
table_name = 'updated_sample_submission'

conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
df = pd.read_csv(csv_file_name)
df.to_csv(csv_file_name, na_rep=np.nan, index=False)
print(f"Here is the shape of the csv file we want to load into the db  {df}")

with conn as conn_create_empy_table:
    cur = conn_create_empy_table.cursor()
    create_table_sql_query = turn_csv_into_sql_table(csv_file_name, schema_name, table_name, save_to_file=False)
    for query in create_table_sql_query:
        cur.execute(query)

df = read_sql_table_to_df(conn, schema_name, table_name)
print(df.head())


# TODO: the algoritm that reads a csv file should be more robust. Please look
# TODO: at python morsels tasks to improve it. And test it on
# test it updated_sample_submission.csv' file, which is particularly difficult
with conn as conn_populate_a_table:
    cur = conn_populate_a_table.cursor()
    with open(csv_file_name, 'r') as file:
        next(file) # skip csv header (first row with column titles)
        reader = csv.reader(file)
        for row in reader:
            # insert row here
            sub_string_s = ', '.join(['%s' for val in row])
            cur.execute(f"INSERT INTO {schema_name}.{table_name} VALUES ({sub_string_s});", row)

df_from_the_db = read_sql_table_to_df(conn, schema_name, table_name)
print(df_from_the_db.head())
print(f"Here is the shape of the table from the postgres database {df_from_the_db.shape}")
