import json
import os


def read_json_file(inputfile):
    try:
        with open(inputfile, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        return {"error": str(e)}


def read_json_by_key(inputfile, key=None):
    try:
        if '.json' in inputfile and key is not None:
            file = read_json_file(inputfile)
            if key in file.keys():
                return file[key]
            else:
                return 'Please select valid key'

        else:
            return 'Please check filename or key and Filename type should be JSON'
    except Exception as e:
        return str(e)


def update_value_by_key(inputfile, key=None, val=None):
    try:
        if '.json' in inputfile and key is not None and val is not None:
            file = read_json_file(inputfile)
            if key in file.keys():

                file[key] = val
                with open(inputfile, "w") as jsonFile:
                    json.dump(file, jsonFile)
                return file
            else:
                return 'Please select valid key'

        else:
            return 'Please check filename or parameters and Filename type should be JSON'

    except Exception as e:
        return str(e)


def add_obj(inputfile, obj=None, key=None, val=None):
    try:
        if '.json' in inputfile and obj is not None and key is not None and val is not None:
            file = read_json_file(inputfile)
            if obj not in file.keys():
                add_obj = {obj: {key: val}}
                file.update(add_obj)
                with open(inputfile, "w") as jsonFile:
                    json.dump(file, jsonFile)
                return file
            else:
                return "object already exists"

        else:
            return 'Please check filename or parameters and Filename type should be JSON'
    except Exception as e:
        return str(e)


def add_key_value(inputfile, key=None, val=None):
    try:
        if '.json' in inputfile and key is not None and val is not None:
            file = read_json_file(inputfile)
            if key not in file.keys():
                add_key_val = {key: val}
                file.update(add_key_val)
                with open(inputfile, "w") as jsonFile:
                    json.dump(file, jsonFile)
                return file
            else:
                return "key already exist"

        else:
            return 'Please check filename or parameters and Filename type should be JSON'
    except Exception as e:
        return str(e)


def delete_obj(inputfile, key=None):
    if '.json' in inputfile and key is not None:
        file = read_json_file(inputfile)

        if key in file.keys():
            del file[key]
            with open(inputfile, "w") as jsonFile:
                json.dump(file, jsonFile)
            return file
        else:
            return 'Please select valid key'

    else:
        return 'Please check filename or parameters and Filename type should be JSON'
