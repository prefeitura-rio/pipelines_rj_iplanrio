from typing import Any

import pandas as pd
from prefect import task
from prefeitura_rio.pipelines_utils.infisical import get_secret
from pymongo import MongoClient
from pymongo.collection import Collection

from pipelines.taxirio.constants import constants
from pipelines.utils import log

CollectionResult = list[dict[str, Any]]


@task
def get_mongo_connection_string() -> str:
    """Get MongoDB connection string."""
    log("Getting MongoDB connection string")

    connection = get_secret(
        secret_name=constants.MONGO_CONNECTION.value,
        path="/taxirio",
    )

    return connection[constants.MONGO_CONNECTION.value]


@task
def get_mongo_client(connection: str) -> MongoClient:
    """Get MongoDB client."""
    log("Getting MongoDB client")

    return MongoClient(connection)


@task
def get_mongo_collection(client: MongoClient, database: str, collection: str) -> Collection:
    """Get MongoDB collection."""
    log("Getting MongoDB collection")

    return client[database][collection]


@task
def get_collection_data(collection: Collection) -> CollectionResult:
    """Get data from MongoDB."""
    log("Getting data from MongoDB")

    return list(collection.find())


@task
def convert_to_df(data: CollectionResult) -> pd.DataFrame:
    """Convert data to DataFrame."""
    log("Converting data to DataFrame")

    return pd.DataFrame(data).drop("_id", axis=1)


@task
def save_to_csv(dataframe: pd.DataFrame) -> None:
    """Save data to .csv file."""
    log("Saving data to .csv")

    dataframe.to_csv("cities.csv", index=False)
