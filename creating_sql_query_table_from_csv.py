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
        'float64': 'NUMERIC',
        'int64': 'NUMERIC',
}

colnames_types_sql_types = {}
for i, col in enumerate(df.columns):

    columntype = str(df[col].dtype)
    sql_type = translating_dtypes_to_sqldatatypes.get(columntype, "varchar")

    if sql_type == "varchar":
        max_size = colnames_maxlenght_dict.get(col, 1024)
        sql_type = "varchar" + f"({max_size})"
    flag = re.findall(r"\s", col)
    if flag:
        col = "\'" + col + "\'"

    colnames_types_sql_types[col] = sql_type

print(colnames_types_sql_types)


columns_and_types_sql_query = ' '.join([" " +key+" " +values + " NULL, \n"
                                       for key,values in colnames_types_sql_types.items()])[:-3]



output_sql =  f"""
CREATE TABLE {schema_name}.{table_name} (
	{columns_and_types_sql_query}
);"""
print(output_sql)


with open(f"create_{table_name}_table_sql_query.sql", "w") as sql_file:
    sql_file.write(output_sql)