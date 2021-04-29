

# external imports
import psycopg2
import csv
import os
import pandas as pd
import numpy as np
import sys
from tqdm import tqdm

#internal imports
from creating_sql_query_table_from_csv import turn_csv_into_sql_table
from load_data_to_pandas_from_postgres_database import read_sql_table_to_df
from removing_forbidden_characters_from_filenames import removing_unwanted_characters
# TODO: Using the prepare sql statement to accelerate the sql query execution


# define a function that handles and parses psycopg2 exceptions
def print_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")


def clean_row(row: list):

    for index,val in enumerate(row):
    if val == '':
        row[index] = np.nan

    return row



def check_connection(conn):
    flag = conn.closed
    flag_str = "closed" if flag else "open"
    return f"The connection to the db is {flag_str}"


csv_file_name = r'data/RFNSA AUS Tower Database.csv'
hostname = os.environ.get('HOST_POSTGRES') #'localhost' #
username = os.environ.get('DB_USER') #'postgres' #
password = os.environ.get('DB_PASS') #os.environ.get('DB_PASS_LOCAL') #
database = 'reference'
schema_name = 'staging_asiapac'
table_name = removing_unwanted_characters('RFNSA AUS Tower Database').lower()

try:
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

    # TODO: test it updated_sample_submission.csv' file, which is particularly difficult

    with conn as conn_populate_a_table:
        cur = conn_populate_a_table.cursor()
        with open(csv_file_name, 'r') as file:
            next(file) # skip csv header (first row with column titles)
            reader = csv.reader(file)
            for row_nb,row in tqdm(enumerate(reader)):
                # insert row here
                sub_string_s = ', '.join(['%s' for val in row])
                cur.execute(f"INSERT INTO {schema_name}.{table_name} VALUES ({sub_string_s});", clean_row(row))

    df_from_the_db = read_sql_table_to_df(conn, schema_name, table_name)
    print(df_from_the_db.head())
    print(f"Here is the shape of the table from the postgres database {df_from_the_db.shape}")

except Exception as err:
    print("Oops! An exception has occured:", err)
    print("Exception TYPE:", type(err))
    print_psycopg2_exception(err)

finally:
    conn.close()
print(check_connection(conn))
