import collections
import csv
import json


def convert_hash_map_values_into_sheet_column_dictionary(*dicts):
    data = collections.defaultdict(list)
    for d in dicts:
        for entry in d:
            for k, v in entry.iteritems():
                data[k].append(v)
    return dict(data)


def get_csv_data(file_name):
    try:
        data = read_csv_data_into_hashmap(file_name)
        return convert_hash_map_values_into_sheet_column_dictionary(data)
    except IOError:
        return "File does not exist"
    except Exception as e:
        return e


def read_csv_data_into_hashmap(file_name):
    with open(file_name, 'r') as f:
        google_sheet_data = json.load(f)
    return google_sheet_data


def write_csv_data_to_hash_map(file_path):
    """
    :param file_path:
    :return:
    all csv file data into hashmap forms
    """
    try:
        with open(file_path, 'r') as file:
            row_column_data = []
            csv_file = csv.DictReader(file)
            for row in csv_file:
                row_column_data.append(dict(row))

        return row_column_data
    except IOError:
        return "File not found"


def get_csv_data_by_column_name(json_csv_file_path, column_name):
    csv_data = get_csv_data(json_csv_file_path)
    if column_name in csv_data.keys():
        return {column_name: csv_data[column_name]}
    else:
        return "Invalid column name"


def get_csv_column_names(file_path):
    """
    :param file_path:
    :return:
    list of all column in csv file.
    """
    try:

        with open(file_path, 'r') as file:
            csv_file = csv.DictReader(file)
            return csv_file.fieldnames
    except IOError:
        return "File does not exist"
    except Exception as e:
        return e


def check_csv_column_name_exist(file_path, column_name):
    """
    :param file_path:
    :param column_name:
    :return: True if column exist in csv file.
    """
    all_column_list = get_csv_column_names(file_path)
    if column_name in all_column_list:
        return True
    else:
        return False


def get_csv_sheet_data_by_column_index(file_path, col_index):
    """
    :param file_path:
    :param col_index:
    :return
    sheet data by column index
    """
    try:

        with open(file_path, "r") as csv_file:
            col_data = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            for lines in csv_reader:
                col_data.append(lines[col_index])
            return {col_index: col_data[1:]}
    except IOError:
        return "File does not exist"
    except IndexError:
        return "Invalid column index"


def get_csv_sheet_data_by_row_index(file_path, row_index):
    """
    :param file_path: csv file path
    :param row_index: row index
    :return:
    """
    try:
        rows_data = write_csv_data_to_hash_map(file_path)
        if row_index <= len(rows_data):
            return rows_data[row_index]
        else:
            return "Invalid row index"
    except Exception as e:
        return e


def get_csv_sheet_data_by_column_name(file_path, col_name):
    """
    :param file_path:
    :param col_name:
    :return:
    get sheet data by column name.
    """
    try:
        all_columns = get_csv_column_names(file_path)
        with open(file_path, "r") as csv_file:
            if col_name in all_columns:
                col_data = []
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for lines in csv_reader:
                    col_data.append(lines[col_name])
                return {col_name: col_data}
            else:
                return "Invalid column name"
    except IOError:
        return "File does not exist"
    except Exception as e:
        return (e, ".....error")


def check_key_present_in_csv_column(file_path, col_name, key):
    """
    :param file_path:
    :param col_name:
    :param key:
    :return:
    True if column key present in respective column.
    """
    try:
        all_columns = get_csv_column_names(file_path)
        if col_name in all_columns:
            col_data = get_csv_sheet_data_by_column_name(file_path, col_name)
            if key in col_data[col_name]:
                return True
            else:
                return False
        else:
            return "Invalid column name"
    except IOError:
        return "File does not exist"
    except Exception as e:
        return e
