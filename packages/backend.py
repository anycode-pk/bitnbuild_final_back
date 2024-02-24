from packages import app
from flask_cors import cross_origin
from flask import request, jsonify
import os
import json
import pandas as pd
import os
import atexit
from checksumdir import dirhash
from apscheduler.schedulers.background import BackgroundScheduler

DATABASE_DIR = 'databases/'
IMAGES_DIR = 'images/'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("packages", "")
PANDAS_DB = None
DATABASE_DIR_HASH = dirhash(ROOT_DIR + DATABASE_DIR, 'md5')


def folder_changes():
    global DATABASE_DIR_HASH
    new_hash = dirhash(ROOT_DIR + DATABASE_DIR, 'md5')
    if new_hash != DATABASE_DIR_HASH:
        DATABASE_DIR_HASH = new_hash
        return True
    return False


def update_pandas():
    global PANDAS_DB
    if folder_changes():
        PANDAS_DB = None
        init_pandas()


def parse_json(JSON_PATH):
    with open(JSON_PATH) as f:
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
        item_name = item["id"].replace("minecraft:", "").replace("_", " ").title()
        item_image = ROOT_DIR + IMAGES_DIR + item["id"].replace("minecraft:", "") + ".png"
        tag = item.get("tag", None)
        tag_potion = None
        if tag:
            tag_potion = tag.get("Potion", None)
            tag_damage = tag.get("Damage", None)
        else:
            tag_damage = None
        extracted_data.append((x, y, z, count, slot, item_id, item_name, item_image, tag_potion, tag_damage, chest_id))
    return extracted_data


def init_pandas():
    global PANDAS_DB
    if PANDAS_DB is None:
        for filename in os.listdir(DATABASE_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(DATABASE_DIR, filename)
                new_data = parse_json(file_path)
                new_df = pd.DataFrame(new_data, columns=["x", "y", "z", "count", "slot", "item_id", "item_name", "item_image", "tag_potion", "tag_damage", "chest_id"])
                PANDAS_DB = pd.concat([PANDAS_DB, new_df], ignore_index=True)
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
        grouped_data = PANDAS_DB.groupby("item_name").agg({"count": "sum", "item_image": "first"}).reset_index()
        result_dict = grouped_data.to_dict(orient="records")
        return jsonify(result_dict)


@app.route('/all', methods=['GET'])
@cross_origin()
def all_data():
    init_pandas()
    if request.method == 'GET':
        result_dict = PANDAS_DB.to_dict(orient="records")
        return jsonify(result_dict)


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_pandas, trigger="interval", seconds=5)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())