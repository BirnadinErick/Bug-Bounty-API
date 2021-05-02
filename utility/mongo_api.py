from pymongo import MongoClient
from .const import MONGODB_CONN_STR

mdb_api = None


def connect():
    global mdb_api
    mdb_api = MongoClient(MONGODB_CONN_STR)  # mongo db conn api


def reconnect():
    global mdb_api
    del mdb_api
    connect()


if __name__ == "__main__":
    from .exceptions import UseAsModule
    raise UseAsModule
else:
    connect()
