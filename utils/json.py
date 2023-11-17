import json

def read_json_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data