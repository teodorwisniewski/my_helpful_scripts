
import glob
import pandas as pd
import pathlib
import os
import warnings
from typing import List, Union
import subprocess
import inspect


def get_caller_info():
  # first get the full filename (including path and file extension)
  caller_frame = inspect.stack()[1]
  caller_filename_full = caller_frame.filename

  # now get rid of the directory (via basename)
  # then split filename and extension (via splitext)
  caller_filename_only = os.path.splitext(os.path.basename(caller_filename_full))[0]

  # return both filename versions as tuple
  return caller_filename_full, caller_filename_only


def wb_styling(writer):
    _, filename = get_caller_info()
    workbook_results = writer.book
    workbook_results.set_properties({
        'title': f'This is the ouput of the script {filename} written by Teodor Wisniewski',
        'subject': 'With document properties',
        'author': 'Teodor Wisniewski for',
        'manager': '',
        'company': '',
        'category': 'Example spreadsheets',
        'keywords': 'Sample, Example, Properties',
        'comments': 'The code was written in python in 2021'})

    return writer


def transform_csv_files_to_excel_file(list_of_csv_files:List[Union[str, bytes, os.PathLike]] = None,
                                      output_path_excel: str = "output.xlsx",
                                      sheet_names: List[str] = None,
                                      open_output_file=True):
    """
    This function allows to load list of csv files and returns
    :param list_of_csv_files: a container of paths to csv files you want to load to your csv filke
    :param output_path_excel: the path to your output excel file
    :param sheet_names: Sheets names are the same as input ccsv files. One can define oother sheetnames that have to be
    defined in the same order as the files in the list_of_csv_files parameter.
    :return: None The function create a new excel file with results.
    """

    with pd.ExcelWriter(output_path_excel, engine='xlsxwriter') as writer:
        writer = wb_styling(writer)
        for i,csv_file in enumerate(list_of_csv_files):

            df = pd.read_csv(csv_file)
            if sheet_names is None:
                sheet_name = os.path.basename(csv_file).split('.')[0][:31]
            else:
                sheet_name = sheet_names[i]
            if len(sheet_name)>31:
                warnings.warn("The sheetname {sheet_name} for {csv_file} is too long. The sheet name will be truncated to 31 characters.")

            df.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column('A:AZ', 25)
            print(f"saving the {csv_file} to the file {output_path_excel}")
    print(f"End The following list of files {list_of_csv_files} has been loaded to the {output_path_excel}")
    if open_output_file:
        try:
            subprocess.Popen(os.path.normpath(output_path_excel), shell=True)
        except Exception as e:
            print(str(e))



if __name__ == "__main__":
    list_of_csv_files = glob.glob(r"data/*.csv")
    transform_csv_files_to_excel_file(list_of_csv_files)
    print(list_of_csv_files)