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


data_path = os.path.join(os.getcwd(), "database/data")
os.makedirs(data_path, exist_ok=True)

def get_user_data(user):
    path = os.path.join(data_path, f"{user}.json")
    return open_json(path)

def set_user_data(user, data):
    path = os.path.join(data_path, f"{user}.json")
    return write_json(path, data)