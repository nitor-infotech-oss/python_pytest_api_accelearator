import xlrd
from xlrd.biffh import XLRDError
from pandas import *


def get_all_sheets(file_name):
    """
    :param file_name:
    :return:
    All sheet names list
    """
    try:
        excel_obj = xlrd.open_workbook(file_name)
        excel_sheets = excel_obj.sheet_names()
        return excel_sheets
    except Exception as e:
        return e


def get_sheet_data_by_sheet_name(file_name, sheet_name):
    """
    :param file_name:
    :param sheet_name:
    :return:
    """
    try:
        all_sheet_names = get_all_sheets(file_name)
        if sheet_name in all_sheet_names:
            sheet_data = get_sheet_data(file_name, None, sheet_name)
            return sheet_data
        else:
            return 'Invalid sheet name'
    except Exception as e:
        return e


def get_sheet_data_by_sheet_index(file_name, index):
    """
    :param file_name:
    :param index:
    :return:
    all sheet data by sheet index
    """
    try:
        sheet_data = get_sheet_data(file_name, index)
        return sheet_data
    except IndexError:
        return {"err": "please enter valid sheet index"}
    except Exception as e:
        return e, "......error"


def get_sheet_data_by_sheet_column_index(file_name, sheet_index=0, col_idx=0):
    """
    :param file_name:
    :param sheet_index:
    :param col_idx:
    :return:
    get column data by column index
    """
    try:
        excel_obj = xlrd.open_workbook(file_name)
        if sheet_index <= excel_obj.nsheets:
            excel_sheets = excel_obj.sheet_by_index(sheet_index)
            col_data = excel_sheets.col_values(col_idx)
            column_index_data = {col_data[0]: col_data[1:]}
            return column_index_data
        else:
            return "Invalid sheet index"
    except IndexError:
        return "please enter valid column index"
    except Exception as e:
        return e


def get_sheet_data_by_column_name(file_name, sheet_index, col_name):
    """
    :param file_name:
    :param sheet_index:
    :param col_name:
    :return:
    return sheet data by column name
    """
    try:
        sheet_data = get_sheet_data(file_name, sheet_index)
        if col_name in sheet_data[0]:
            column_data = sheet_data[0][col_name]
            return {col_name: column_data}
        else:
            return "Invalid column name"
    except Exception as e:
        return e


def get_sheet_data(file_name, sheet_index=None, sheet_name=None):
    """
    :param file_name:
    :param sheet_index:
    :return:
    return all sheet data in hash map forms
    """
    try:
        excel_obj = xlrd.open_workbook(file_name)
        if sheet_index is not None:
            if sheet_index < len(excel_obj.sheets()):
                excel_sheets = excel_obj.sheet_by_index(sheet_index)
                sheet_data = create_dictionary(excel_sheets)
                return {sheet_index: sheet_data}
            else:
                return "invalid sheet index"
        if sheet_name is not None:
            excel_sheets = excel_obj.sheet_by_name(sheet_name)
            sheet_data = create_dictionary(excel_sheets)
            return {sheet_name: sheet_data}
    except IndexError:
        return "Invalid sheet index"
    except Exception:
        return "please enter valid sheet index"


def create_dictionary(excel_sheets):
    sheet_data = {}
    for col in range(excel_sheets.ncols):
        for row in range(excel_sheets.nrows):
            sheet_data[excel_sheets.row_slice(0)[col].value] = excel_sheets.col_values(col)[1:]
    return sheet_data


def check_key_present_in_column(file_name, sheet_index, col_idx, key):
    """
    :param file_name:
    :param sheet_index:
    :param col_idx:
    :param key:
    :return:
    check specific key present in column.
    """
    excel_obj = xlrd.open_workbook(file_name)
    excel_sheets = excel_obj.sheet_by_index(sheet_index)
    if key in excel_sheets.col_values(col_idx, 1, excel_sheets.nrows):
        return True
    else:
        return False


def get_sheet_data_by_row_index(file_name, sheet_index, row_index):
    """
    :param file_name:
    :param sheet_index:
    :param row_index:
    :return:
    sheet data by row index
    """
    excel_obj = xlrd.open_workbook(file_name).sheet_by_index(sheet_index)
    row_data = excel_obj.row(row_index)
    return row_data


def get_sheet_data_by_row_column(file_name, sheet_index, row_index):
    """
    :param file_name:
    :param sheet_index:
    :param row_index:
    :return:
    sheet data with row_column hash map forms
    """

    excel_obj = xlrd.open_workbook(file_name).sheet_by_index(sheet_index)
    row_column_data = {}
    no_of_columns = excel_obj.ncols
    for i in range(no_of_columns):
        row_column_data[excel_obj.row(0)[i].value] = excel_obj.row(row_index)[i].value
    return row_column_data


def get_sheet_data_into_hashmap(file_name, sheet_index=None, sheet_name=None):
    """
    :param sheet_name:
    :param file_name:
    :param sheet_index:
    :param row_index:
    :return:
    sheet data with row_column hash map forms
    """
    try:
        if sheet_index is not None:
            excel_obj = xlrd.open_workbook(file_name).sheet_by_index(sheet_index)
            keys = [excel_obj.cell(0, col_index).value for col_index in range(excel_obj.ncols)]
            row_col_hashed = []
            for row_index in range(1, excel_obj.nrows):
                d = {keys[col_index]: excel_obj.cell(row_index, col_index).value
                     for col_index in range(excel_obj.ncols)}
                row_col_hashed.append(d)
            return {sheet_index: row_col_hashed}
        if sheet_name is not None:
            excel_obj = xlrd.open_workbook(file_name).sheet_by_name(sheet_name)
            all_sheet_names = get_all_sheets(file_name)
            if sheet_name in all_sheet_names:
                keys = [excel_obj.cell(0, col_index).value for col_index in range(excel_obj.ncols)]
                row_col_hashed = []
                for row_index in range(1, excel_obj.nrows):
                    d = {keys[col_index]: excel_obj.cell(row_index, col_index).value
                         for col_index in range(excel_obj.ncols)}
                    row_col_hashed.append(d)
                return {sheet_name: row_col_hashed}
    except IndexError:
        return "Invalid sheet index"
    except XLRDError:
        return "Invalid sheet name"
    except Exception as e:
        return e


def get_all_column_names(file_name, sheet_index):
    """
    :param file_name:
    :param sheet_index:
    :return:
    All sheet column names
    """
    try:
        excel_obj = xlrd.open_workbook(file_name).sheet_by_index(sheet_index)
        return {'all_col_names': excel_obj.row_values(0)}
    except Exception as e:
        return e


def check_column_name_exist(file_name, sheet_index, column_name):
    """
    :param file_name:
    :param sheet_index:
    :param column_name:
    :return:
    return True if column exist in sheet
    """
    try:
        excel_obj = xlrd.open_workbook(file_name).sheet_by_index(sheet_index)
        if column_name in excel_obj.row_values(0):
            return True
        else:
            return False
    except Exception as e:
        return e

