from packages import app
from flask_cors import cross_origin
from flask import request
import os
import json
import pandas as pd

DATABASE_DIR = 'databases/'
JSON_NAME = 'items.json'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("packages", "")
PANDAS_DB = None


def parse_json():
    with open(ROOT_DIR + DATABASE_DIR + JSON_NAME) as f:
        data = json.load(f)
    items = data["Items"]
    chest_id = data["id"]
    x = data["x"]
    y = data["y"]
    z = data["z"]

    # Create a list to hold the extracted data
    extracted_data = []

    # Iterate through the items and extract relevant information
    for item in items:
        count = item["Count"]
        slot = item["Slot"]
        item_id = item["id"]
        tag = item.get("tag", None)
        tag_potion = None
        if tag:
            tag_potion = tag.get("Potion", None)
            tag_damage = tag.get("Damage", None)
        else:
            tag_damage = None
        extracted_data.append((x, y, z, count, slot, item_id, tag_potion, tag_damage, chest_id))
    return extracted_data


def init_pandas():
    global PANDAS_DB
    if PANDAS_DB is None:
        extracted_data = parse_json()
        PANDAS_DB = pd.DataFrame(extracted_data, columns=["x", "y", "z", "count", "slot", "item_id", "tag_potion", "tag_damage", "chest_id"])
    if PANDAS_DB is None:
        raise Exception('No File to parse. Put it in databases/ folder as items.json')
    print(PANDAS_DB.to_string())


@app.route('/')
@cross_origin()
def index():
    init_pandas()
    return 'test'


@app.route('/items', methods=['GET'])
@cross_origin()
def items():
    init_pandas()
    if request.method == 'GET':
        grouped_data = PANDAS_DB.groupby("item_id")["count"].sum().reset_index()

# Convert the grouped data to a dictionary
result_dict = grouped_data.to_dict(orient="records")
    return 'test'
