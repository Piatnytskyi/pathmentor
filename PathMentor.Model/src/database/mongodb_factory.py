import tensorflow_io as tfio
from pymongo import MongoClient
import urllib.parse

class MongoDBFactory:
    def __init__(self):
        self._client = None

    def get_client(self, database_uri):
        if self._client is None:
            self._client = MongoClient(database_uri)
        return self._client

    def create_writer(self, database_uri, database, collection):
        return tfio.experimental.mongodb.MongoDBWriter(uri=database_uri, database=database, collection=collection)
