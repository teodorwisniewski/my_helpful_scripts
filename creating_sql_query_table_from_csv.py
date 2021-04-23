# Script created by Teodor Wisniewski

#imports
import pandas as pd
import re
from removing_forbidden_characters_from_filenames import removing_unwanted_characters


def detecting_geometry_object(cell_value: str) -> str:
    """
    This function detects if a datapoint is a postGIS geometry object
    :param cell_value: a data point, which normally is a strng
    :return: return '' noting or string with a corresponding geometry object
    """
    if not isinstance(cell_value, (str,)):
        return ''

    geometry_objects_list = ['POINT'.lower(), 'LINESTRING'.lower(), 'POLYGON'.lower(), 'MultiPoint'.lower(),
                             'MULTILINESTRING'.lower(), 'MULTIPOLYGON'.lower()]
    used_geom_objects = [geom_obj for geom_obj in geometry_objects_list if geom_obj in cell_value.lower()]
    # flag = True if used_geom_objects else False
    output_value = used_geom_objects[-1].upper() if len(used_geom_objects) > 0 else ''
    return output_value


def get_object_columns_max_lenght(df_to_check: pd.DataFrame) -> dict:
    colnames_maxlenght_dict = {}
    for i, c in enumerate(df_to_check.columns):
        if df_to_check[c].dtype == 'object':
            max_lenght_str = df_to_check[c].str.len().max()
            colnames_maxlenght_dict[c] = int(max_lenght_str)

    return colnames_maxlenght_dict


def formatting_output_sql_column_name(colname:str) ->str:
    # rowing unwanted character and lowering column names
    colname = removing_unwanted_characters(colname, all_dots=True).lower()
    flag = re.findall(r"[^a-zA-Z0-9\_]", colname)
    if flag:
        colname = '\"' + colname + '\"'
    return colname


def define_varchar_sql_type(df_to_process: pd.DataFrame,
                            colnames_maxlenght_dict: dict,
                            colname:str):
    max_size = colnames_maxlenght_dict.get(colname, 1024)
    sql_type = "varchar" + f"({max_size})"
    data_point = df_to_process[colname].iloc[0]
    if geom_type := detecting_geometry_object(data_point):
        sql_type = f"geometry({geom_type}, 4326)"
    return sql_type


def df_column_types_to_sql_datatypes(df_to_process: pd.DataFrame) -> dict:
    """
    This function takes as an input a dataframe object and return a dict
    with column names and corresponding datatypes in sql
    :param df_to_process: pandas.Dataframe object th
    :return: a dict for instance:
    colnames_types_sql_types= {'meetid': 'int8',
    'meetpath': 'varchar(47)',
    'federation': 'varchar(14)',
    'date': 'varchar(10)',
    'meetcountry': 'varchar(17)',
    'meetstate': 'varchar(3)',
    'meettown': 'varchar(49)',
     'meetname': 'varchar(156)'}

    """
    translating_dtypes_to_sqldatatypes = {
            'object': 'varchar',
            'float64': 'float8', # 15 decimal digits precision
            'int64': 'int8',
    }
    colnames_maxlenght_dict = get_object_columns_max_lenght(df_to_process)
    colnames_types_sql_types = {}
    for i, col in enumerate(df_to_process.columns):
        columntype = str(df_to_process[col].dtype)
        sql_type = translating_dtypes_to_sqldatatypes.get(columntype, "varchar")
        if sql_type == "varchar": sql_type = define_varchar_sql_type(df_to_process,colnames_maxlenght_dict,col)
        col = formatting_output_sql_column_name(col)
        colnames_types_sql_types[col] = sql_type

    return colnames_types_sql_types


def turn_csv_into_sql_table(csv_filename:str, schema_name:str, table_name:str,
                            save_to_file: bool = True,
                            drop_table_if_exists: bool = True,
                            clean_special_characters_in_sql:bool =True,
                            save_to_csv_df_copy: bool = True) -> list:
    """

    :param clean_special_characters_in_sql: removes "\n" and "\t" from output string
    :param drop_table_if_exists: if True adds a line to the output sql query "DROP TABLE IF EXISTS schema.table"
    :param save_to_file: True if want to save an sql query in a sql file
    :param csv_filename: contains path to the csv file based on which we want to create a sql table
    :param schema_name: the name of schema in our postgres database
    :param table_name: the name of a table in the postgres database
    :param save_to_csv_df_copy: it allows to save a csv copy of dataframe with properly formatted columns
    :return: it returns a string with a new sql query that enables to create a table. For instance:

    CREATE TABLE public.happiness2021 (
                meetid int8 NULL,
                meetpath varchar(47) NULL,
                federation varchar(14) NULL,
                date varchar(10) NULL,
                meetcountry varchar(17) NULL,
                meetstate varchar(3) NULL,
                meettown varchar(49) NULL,
                meetname varchar(156) NULL
    );

    """
    df = pd.read_csv(csv_filename)
    colnames_types_sql_types = df_column_types_to_sql_datatypes(df)
    columns_and_types_sql_query = ''.join(["\t\t\t" +key+" " +values + " NULL, \n"
                                           for key,values in colnames_types_sql_types.items()])[:-3]
    output_sql =f"""CREATE TABLE {schema_name}.{table_name} (
    {columns_and_types_sql_query});"""

    drop_table_sql = f"DROP TABLE IF EXISTS {schema_name}.{table_name}; \n"
    print(drop_table_sql + output_sql)

    if save_to_csv_df_copy:
        new_col_names = [formatting_output_sql_column_name(col) for col in df.columns]
        df_to_process = df.rename(columns=dict(zip(df.columns, new_col_names)))
        df_to_process.to_csv(csv_filename, index=False)

    if save_to_file:
        with open(f"create_{table_name}_table_sql_query.sql", "w") as sql_file:
            sql_file.write(drop_table_sql + output_sql)

    if clean_special_characters_in_sql:
        drop_table_sql = drop_table_sql.replace("\n", " ").replace("\t", "    ")
        output_sql = output_sql.replace("\n", " ").replace("\t", "    ")

    if drop_table_if_exists:
        output_table = [drop_table_sql]
    else:
        output_table = []
    output_table.append(output_sql)

    return output_table








if __name__ == "__main__":
    # Fill out this variables adequately
    schema_name = 'public'
    table_name = 'file_name'
    csv_filename = 'file_name.csv'
    out_str = turn_csv_into_sql_table(csv_filename, schema_name, table_name)
    print(out_str)