from collections.abc import Generator, ItemsView
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import pandas as pd
from prefeitura_rio.pipelines_utils.infisical import get_secret
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from pipelines.taxirio.constants import Constants
from pipelines.taxirio.types import QueryResult
from pipelines.utils import log


def get_mongo_connection_string() -> str:
    """Get MongoDB connection string."""
    log("Getting MongoDB connection string")

    connection = get_secret(
        secret_name=Constants.MONGO_CONNECTION.value,
        path="/taxirio",
    )

    return connection[Constants.MONGO_CONNECTION.value]


def get_mongo_client(connection: str) -> MongoClient:
    """Get MongoDB client."""
    log("Getting MongoDB client")

    return MongoClient(connection)


def get_mongo_collection(client: MongoClient, database: str, collection: str) -> Collection:
    """Get MongoDB collection."""
    log("Getting MongoDB collection")

    return client[database][collection]


def get_collection_data(collection: Collection) -> QueryResult:
    """Get data from MongoDB."""
    log("Getting data from MongoDB")

    return list(collection.find())


def get_collection_data_in_batches(collection: Collection, batch_size: int) -> Cursor:
    """Get data from MongoDB in batches."""
    log("Getting data from MongoDB in batches")

    return collection.find(batch_size=batch_size)


def convert_to_df(data: QueryResult | ItemsView[str, Any]) -> pd.DataFrame:
    """Convert data to DataFrame."""
    log("Converting data to DataFrame")

    return pd.DataFrame(data)


def use_df_first_row_as_header(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Use the first row as header."""
    log("Using the first row as header")

    dataframe.columns = dataframe.iloc[0]

    return dataframe.drop([0], axis=0)


def save_to_csv(dataframe: pd.DataFrame, name: str) -> Path:
    """Save data to .csv file."""
    log("Saving data to .csv")

    path = Path(f"output/{name}.csv")

    path.parent.mkdir(exist_ok=True)

    dataframe.to_csv(path, index=False)

    return path


@contextmanager
def log_dump_collection(name: str, level: str = "info") -> Generator:
    """Log a message before and after a dump collection operation."""
    try:
        log(f"Dumping {name} collection", level)
        yield
    finally:
        log(f"Finished {name} dump", level)
