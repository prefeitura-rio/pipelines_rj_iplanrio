from dataclasses import dataclass, field

from pymongo import MongoClient
from pymongo.collection import Collection

from pipelines.taxirio.constants import constants
from pipelines.utils import get_env_variable


def _mongo_client() -> MongoClient:
    """Get a MongoDB client."""
    return MongoClient(get_env_variable("DB_CONNECTION_STRING"))


@dataclass(frozen=True)
class MongoTaxiRio:
    """Class to handle MongoDB connections for the taxirio project."""

    client: MongoClient = field(default_factory=_mongo_client)

    def get_collection(self, collection: str) -> Collection:
        """Get a MongoDB collection by name."""
        database = self.client[constants.TAXIRIO_MONGODB_NAME.value]

        return database[collection]
