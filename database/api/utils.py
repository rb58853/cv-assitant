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
            return json.loads(file.write(json.dumps(json_value)))
    except FileNotFoundError:
        raise Exception("File not found.")


data_path = os.path.join(os.getcwd(), "database/data")


def get_user_data(user):
    for file in os.listdir(data_path):
        path = os.path.join(data_path, file)
        if file == f"{user}.json":
            return open_json(path)

def set_user_data(user, data):
    for file in os.listdir(data_path):
        path = os.path.join(data_path, file)
        if file == f"{user}.json":
            return write_json(path, data)