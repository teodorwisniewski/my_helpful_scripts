# Script created by Teodor Wisniewski

#imports
import pandas as pd
import numpy as np
import glob
import os

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

    colnames_types_sql_types[col] = sql_type

print(colnames_types_sql_types)








f"""
CREATE TABLE {schema_name}.{table_name} (
	rmpostcode varchar(8) NULL,
	post_sector varchar(6) NULL,
	eastings int4 NULL,
	northings int4 NULL,
	coa_code varchar(9) NULL,
	lsoa varchar(9) NULL,
	msoa_and_im varchar(9) NULL,
	la_name varchar(50) NULL,
	la_code varchar(50) NULL,
	government_region varchar(15) NULL,
	country varchar(8) NULL,
	households float8 NULL,
	population float8 NULL,
	bus_sites_total float8 NULL,
	premises float8 NULL,
	exchange_name varchar(30) NULL,
	in_cable_franchise_area varchar(1) NULL,
	cable_postcode varchar(1) NULL,
	broadband_tech_available int4 NULL,
	nga_tech_offered_by_bt varchar(50) NULL,
	nga_activation_date varchar(50) NULL,
	alt_net_supplier_code int4 NULL,
	alt_net_supplier_name varchar(16) NULL,
	alt_net_tech_supplied varchar(4) NULL,
	"CityFibre postcode passed" varchar(1) NULL,
	source_of_cable_postcode_flag varchar(32) NULL,
	virgin_rfog varchar(1) NULL,
	virgin_gig1 varchar(1) NULL,
	vm_activation_quarter float8 NULL,
	vm_activation_year float8 NULL,
	multiple_networks_code float8 NULL,
	altnet_deployment_date varchar(18) NULL,
	max_nga_speed float8 NULL
);"""

print(df.columns)
