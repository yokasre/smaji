import pymongo
from pymongo.database import Database
from app.models import DataPoint
from app.db.mongodb import get_mongo_db
import random
import time


def seed_sensor_data() -> None:
    """
    Seeds first data point into mongodb database.
    """

    db: Database = get_mongo_db()
    collection = db["device_data"]

    # Clear collection
    collection.delete_many({})

    # generate data
    data_point_values: dict = {
        "device_id": "100200300400500",
        "temperature": str(random.randint(10, 30)),
        "humidity": str(random.randint(10, 30)),
        "battery": "100",
        "timestamp": int(time.time()),
        "level": "30"
    }
    data_point: DataPoint = DataPoint(**data_point_values)

    # Push to collection
    collection.insert_one(data_point.model_dump())

    print("First data point added successfully.")


def get_last_data_point(device_id: str):
    db: Database = get_mongo_db()
    collection = db["device_data"]
    return collection.find_one({"device_id": device_id}, sort=[("timestamp", pymongo.DESCENDING)])
