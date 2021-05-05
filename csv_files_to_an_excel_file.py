
import glob
import pandas as pd
import pathlib
import os
import warnings
from typing import List, Union
import subprocess
import sys
import inspect
import xlsxwriter
import argparse


# TODO: improve excel formatting


def get_caller_info():
    """
    :return: two strings with path to the script and script name
    """

    # first get the full filename (including path and file extension)
    caller_frame = inspect.stack()[1]
    caller_filename_full = caller_frame.filename

    # now get rid of the directory (via basename)
    # then split filename and extension (via splitext)
    caller_filename_only = os.path.splitext(os.path.basename(caller_filename_full))[0]

    # return both filename versions as tuple
    return caller_filename_full, caller_filename_only


def transform_csv_files_to_excel_file(list_of_csv_files:List[Union[str, bytes, os.PathLike]] = None,
                                      output_path_excel: str = "output.xlsx",
                                      sheet_names: List[str] = None,
                                      open_output_file=True):
    """
    This function allows to load list of csv files and returns
    :param open_output_file: this parameter allows to decide if we want to open the output excel file or not
    :param list_of_csv_files: a container of paths to csv files you want to load to your csv filke
    :param output_path_excel: the path to your output excel file
    :param sheet_names: Sheets names are the same as input ccsv files. One can define oother sheetnames that have to be
    defined in the same order as the files in the list_of_csv_files parameter.
    :return: None The function create a new excel file with results.
    """

    if sheet_names is not None and len(list_of_csv_files) != len(sheet_names):
        warnings.warn(f"The number of csv files is not equal to the number of output excel sheet. \n"
                      f"There are {len(list_of_csv_files)} csv files {list_of_csv_files} \n and"
                      f"There are {len(sheet_names)} sheets{sheet_names} for the output excel files .")
        sheet_names = None

    with pd.ExcelWriter(output_path_excel, engine='xlsxwriter') as writer:
        workbook  = writer.book
        for i,csv_file in enumerate(list_of_csv_files):

            df = pd.read_csv(csv_file)

            if sheet_names is None:
                sheet_name = os.path.basename(csv_file).split('.')[0]
            else:
                sheet_name = sheet_names[i]
            if len(sheet_name)>31:
                warnings.warn(f"The sheetname {sheet_name} created for the {csv_file} file is too long. "
                              f"\nThe sheet name will be truncated to 31 characters.")
                sheet_name = sheet_name[:31]

            df.to_excel(writer, sheet_name=sheet_name, index=False)
            rows, columns = df.shape
            last_column_number = xlsxwriter.utility.xl_col_to_name(columns)
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column('A:' + last_column_number, 20)
            print(f"saving the {csv_file} to the file {output_path_excel}")
    print(f"End The following list of files {list_of_csv_files} has been loaded to the {output_path_excel}")
    if open_output_file:
        try:
            subprocess.Popen(os.path.normpath(output_path_excel), shell=True)
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    caller_filename_full, filename = get_caller_info()
    print(f"Name of the script      : {sys.argv[0]=}")
    print("full path to the script: ", caller_filename_full)
    print(f"Arguments of the script : {sys.argv[1:]=}")
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--output')
    # parser.add_argument('--sheet_names')
    # args = parser.parse_args()
    # my_dict = {'arg1': args.output, 'arg2': args.sheet_names}
    # print("key word arguments", my_dict)
    if len(sys.argv[1:])>0:
        filename = sys.argv[1]
    else:
        filename = "output.xlsx"

    list_of_csv_files = glob.glob(r"data/*.csv")
    transform_csv_files_to_excel_file(list_of_csv_files, output_path_excel = filename)
    print(list_of_csv_files)