import json
import os

"""read data from json file"""
def read_json(filename):

    if not os.path.exists(filename):
        print("JSON file not found.")
        return {}

    with open(filename, "r") as file:
        return json.load(file)

"""Write data to a JSON file."""
def write_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

"""Update a key in a JSON file."""
def update_json(filename, key, value):

    data = read_json(filename)
    data[key] = value
    write_json(filename, data)