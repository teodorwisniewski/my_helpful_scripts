# Teodor's scripts
> This repository contains short and simple scripts that help me to carry out everyday tasks
> at my work

## List of scripts
Here are my scripts:

1. ```removing_forbidden_characters_from_filenames.py```: this script allows to 
replace error-prone filenames with more computer friendly filenames. For instance,
   "some file (fijwef).csv" is replaced with "some_file_fijwef_.csv".
    
2. ```creating_sql_query_table_from_csv.py```: this script allows to create a sql query from csv file. 
   It uses pandas and numpy library. It recognizes correct datatype for each column.

3. ```load_data_to_pandas_from_postgres_database.py``` it allows to load data from a postgres table to a pandas dataframe.
For this script psycopg2 library needs to be installed.

4. ```load_csv_to_postgres_database.py``` it allows to load data from a csv file to a table in the postgres database.
For this script psycopg2, pandas and numpy libraries need to be installed.
   
5. ```csv_files_to_an_excel_file.py``` This scripts transforms several csv files into one Excel file where all csv files 
are in each of corresponding tabs.
   
## Usage
Create and activate a new virtual environment. The scripts were tested with Python 3.8.
Load dependencies required for the usage:
> pip install -r requirements.txt

## Author
Teodor Wisniewski