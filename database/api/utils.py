import json
import os


def open_json(path):
    try:
        with open(path, "r") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        raise Exception("File not found.")


def write_json(path, json_value):
    try:
        with open(path, "w") as file:
            return file.write(json.dumps(json_value))
    except FileNotFoundError:
        raise Exception("File not found.")


def write_fields(file_path, fields: dict):
    """
    Usar solo para json o diccionarios
    """
    with open(file_path, "r+") as file:
        my_value = json.loads(file.read())

    for key in fields:
        my_value[key] = fields[key]

    with open(file_path, "w") as file:
        file.write(json.dumps(my_value))
