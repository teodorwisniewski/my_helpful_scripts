import os
import pandas as pd
import psycopg2


# Simple routine to run a query on a database and print the results:
def do_query(conn, table_name) :
    cur = conn.cursor()
    cur.execute( f"SELECT * FROM {table_name}" )
    query_output_df = display_as_table(cur.fetchall(), cur.description)
    return query_output_df


def display_as_table(data, headers):
    df = pd.DataFrame(data=data, columns=[i[0] for i in headers])
    return df


def read_sql_table_to_df(connection:psycopg2.extensions.connection,
                         schema_name:str,
                         table_name:str) -> pd.DataFrame:
    """
    :param connection: psycopg2 connection
    :param schema_name: schema name in the postgres database
    :param table_name: table name  in the postgres database
    :return:
    """

    with connection as conn:
        df = do_query( my_connection, schema_name + '.' + table_name)
    return df


if __name__ == "__main__":
    # List of variables that have to be defined by users of this script.
    hostname = os.environ.get('HOST_POSTGRES')
    username = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASS')  #
    database = os.environ.get('DATABASE_NAME_POSTGRES')
    schema_name = 'public'
    table_name = 'happiness2021'
    my_connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    df = read_sql_table_to_df(my_connection, schema_name, table_name)
    print(df.head())
