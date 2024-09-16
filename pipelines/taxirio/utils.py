from dataclasses import dataclass, field

from prefeitura_rio.pipelines_utils.infisical import get_secret
from pymongo import MongoClient
from pymongo.collection import Collection

from pipelines.taxirio.constants import constants


@dataclass
class MongoTaxiRio:
    """Class to handle MongoDB connections for the taxirio project."""

    client: MongoClient = field(init=False)

    def __post_init__(self) -> None:
        """Initialize the MongoDB client."""
        connection_string = get_secret(
            secret_name=constants.MONGO_CONNECTION.value,
            path="/taxirio",
        )

        self.client = MongoClient(connection_string[constants.MONGO_CONNECTION.value])

    def get_collection(self, collection: str) -> Collection:
        """Get a MongoDB collection by name."""
        database = self.client[constants.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value]

        return database[collection]
