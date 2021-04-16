# Script created by Teodor Wisniewski

#imports
import pandas as pd
import re


# Fill out this variables adequately
schema_name = 'schema_name'
table_name = 'table_name'
csv_filename = 'file_name.csv'

df = pd.read_csv(csv_filename)
colnames_maxlenght_dict = {}
for i, c in enumerate(df.columns):
    if df[c].dtype == 'object':
        max_lenght_str = df[c].str.len().max()
        print('%s Max length of column %s: %s\n' %  (str(i+1),c, max_lenght_str))
        colnames_maxlenght_dict[c] = int(max_lenght_str)

translating_dtypes_to_sqldatatypes = {
        'object': 'varchar',
        'float64': 'float8', # 15 decimal digits precision
        'int64': 'int8',
}


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


colnames_types_sql_types = {}
for i, col in enumerate(df.columns):

    columntype = str(df[col].dtype)
    sql_type = translating_dtypes_to_sqldatatypes.get(columntype, "varchar")

    if sql_type == "varchar":

        max_size = colnames_maxlenght_dict.get(col, 1024)
        sql_type = "varchar" + f"({max_size})"
        data_point = df[col].iloc[0]
        if geom_type := detecting_geometry_object(data_point):
            sql_type = f"geometry({geom_type}, 4326)"

    flag = re.findall(r"[^a-zA-Z0-9\_]", col)
    if flag:
        col = '\"' + col + '\"'

    colnames_types_sql_types[col] = sql_type

print(colnames_types_sql_types)


columns_and_types_sql_query = ''.join(["\t\t\t" +key+" " +values + " NULL, \n"
                                       for key,values in colnames_types_sql_types.items()])[:-3]



output_sql =f"""
CREATE TABLE {schema_name}.{table_name} (
{columns_and_types_sql_query}
);"""
print(output_sql)


with open(f"create_{table_name}_table_sql_query.sql", "w") as sql_file:
    sql_file.write(output_sql)




