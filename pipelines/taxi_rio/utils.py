from dataclasses import dataclass

from pymongo import MongoClient
from pymongo.collection import Collection

from pipelines.taxi_rio.constants import constants
from pipelines.utils import get_env_variable


@dataclass(frozen=True)
class MongoTaxiRio:
    client: MongoClient = MongoClient(get_env_variable("DB_CONNECTION_STRING"))

    def get_collection(self, collection: str) -> Collection:
        """Get a MongoDB collection by name"""
        database = self.client[constants.TAXI_RIO_MONGODB_NAME.value]

        return database[collection]
