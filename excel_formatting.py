import os
import numpy as np
import inspect
import pandas as pd

import xlsxwriter



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

def column_formatting(worksheet, format, col_nb: int, first_row_nb: int, values):
    for indice, value in enumerate(values):
        if isinstance(value, tuple): value = value[0]
        worksheet.write(first_row_nb + indice, col_nb, value, format)


def row_formatting(worksheet, format, row_nb: int, first_col_nb: int, values):
    for indice, value in enumerate(values):
        worksheet.write(row_nb, first_col_nb + indice, value, format)


def apply_formatting(worksheet, format, first_col_row: tuple, last_col_row: tuple, values):
    """
        first_col_row = (first_row:int, first_column:int)
        last_col_row = (last_row:int, last_column:int)
    """
    if isinstance(values, pd.DataFrame): values = values.values.tolist()
    for value_index, row_nb in enumerate(range(first_col_row[0], last_col_row[0])):
        row_values = values[value_index]
        row_formatting(worksheet, format, row_nb, first_col_row[1], row_values)


def format_sheet(workbook, worksheet, df_calculated):
    rows, columns = df_calculated.shape
    last_column_number = xlsxwriter.utility.xl_col_to_name(columns)
    ################""
    # Sheets formatting
    # first column - index column

    # column_format_dict = {'bold': True, 'font_size': 13, "align": 'center', 'valign': 'vcenter',
    #                       "right": 2  # border
    #                       }
    # format_index_column = workbook.add_format(column_format_dict)
    #
    # column_formatting(worksheet, format_index_column, 0, 0, [df_calculated.index.name] + df_calculated.index.tolist())
    # worksheet.set_column('A:A', 20)
    # proper data column
    format_data = workbook.add_format({'bold': False, "align": 'center', 'font_size': 10, 'valign': 'vcenter',
                                       "left": 2,  # border
                                       "right": 2,  # border
                                       })
    # apply_formatting(worksheet, format_data, (1, 1), (rows + 1, last_column_number), df_calculated.iloc[:, :])
    worksheet.set_column('A:' + last_column_number, 20)
    # Title Row Column titles formatting
    header_format = workbook.add_format({'bold': True, 'align': 'center',
                                         'valign': 'vcenter', 'font_size': 13,
                                         "left": 2,  # border
                                         "right": 2,  # border
                                         "bottom": 2
                                         })

    # row_formatting(worksheet, header_format, 0, 0, [df_calculated.index.name] + list(df_calculated.columns.values))
    worksheet.set_row(0, 25)
    ################""
