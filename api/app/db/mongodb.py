from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

mongo_client: MongoClient = None
mongodb: Database = None


def open_mongodb_connection() -> None:
    """
    Opens a connection to the MongoDB database.
    """

    global mongo_client, mongodb

    if mongo_client is None:
        username: str = quote_plus(os.getenv("MONGO_ATLAS_USERNAME"))
        password: str = quote_plus(os.getenv("MONGO_ATLAS_PASSWORD"))
        db_name: str = os.getenv("MONGO_DB_NAME", "smaji")
        connection_uri: str = f"mongodb+srv://{username}:{password}@smaji-cluster.fk5mzxo.mongodb.net/?appName=smaji-cluster"

        mongo_client = MongoClient(connection_uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)
        mongodb = mongo_client[db_name]

    print("MongoDB connected")


def close_mongodb_connection() -> None:
    """
    Closes the connection to the MongoDB database.
    """

    global mongo_client

    if mongo_client:
        mongo_client.close()
        mongo_client = None
    print("MongoDB closed")


def get_mongo_db() -> Database:
    """
    Returns the MongoDB database instance.
    """

    global mongodb

    if mongodb is None:
        raise Exception("Database connection is not open.")

    return mongodb
