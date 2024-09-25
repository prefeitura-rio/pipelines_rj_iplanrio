from pathlib import Path
from typing import Any

import pandas as pd
from prefect import task
from prefeitura_rio.pipelines_utils.infisical import get_secret
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from pipelines.taxirio.constants import Constants
from pipelines.utils import log

QueryResult = list[dict[str, Any]]


@task
def get_mongo_connection_string() -> str:
    """Get MongoDB connection string."""
    log("Getting MongoDB connection string")

    connection = get_secret(
        secret_name=Constants.MONGO_CONNECTION.value,
        path="/taxirio",
    )

    return connection[Constants.MONGO_CONNECTION.value]


@task(checkpoint=False)
def get_mongo_client(connection: str) -> MongoClient:
    """Get MongoDB client."""
    log("Getting MongoDB client")

    return MongoClient(connection)


@task(checkpoint=False)
def get_mongo_collection(client: MongoClient, database: str, collection: str) -> Collection:
    """Get MongoDB collection."""
    log("Getting MongoDB collection")

    return client[database][collection]


@task(checkpoint=False)
def get_collection_data(collection: Collection, batch: int | None = None) -> QueryResult | Cursor:
    """Get data from MongoDB."""
    log("Getting data from MongoDB")

    if batch:
        return collection.find(batch_size=batch)

    return list(collection.find())


@task
def convert_to_df(data: QueryResult) -> pd.DataFrame:
    """Convert data to DataFrame."""
    log("Converting data to DataFrame")

    return pd.DataFrame(data)


@task
def save_to_csv(dataframe: pd.DataFrame, name: str) -> Path:
    """Save data to .csv file."""
    log("Saving data to .csv")

    path = Path(f"output/{name}.csv")

    path.parent.mkdir(exist_ok=True)

    dataframe.to_csv(path, index=False)

    return path
