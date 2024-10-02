from pathlib import Path
from typing import Any

import pyarrow.parquet as pq
from prefect import task
from prefeitura_rio.pipelines_utils.infisical import get_secret
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongoarrow.api import Schema, aggregate_arrow_all

from pipelines.taxirio.constants import Constants
from pipelines.utils import log


@task(checkpoint=False)
def get_mongodb_connection_string() -> str:
    """Get MongoDB connection string."""
    log("Getting MongoDB connection string")

    connection = get_secret(
        secret_name=Constants.MONGODB_CONNECTION_STRING.value,
        path="/taxirio",
    )

    return connection[Constants.MONGODB_CONNECTION_STRING.value]


@task(checkpoint=False)
def get_mongodb_client(connection: str) -> MongoClient:
    """Get MongoDB client."""
    log("Getting MongoDB client")

    return MongoClient(connection)


@task(checkpoint=False)
def get_mongodb_collection(client: MongoClient, database: str, collection: str) -> Collection:
    """Get MongoDB collection."""
    log("Getting MongoDB collection")

    return client[database][collection]


@task(checkpoint=False)
def dump_collection_from_mongodb(
    collection: Collection,
    path: str,
    schema: Schema,
    pipeline: list[dict[str, Any]],
) -> Path:
    """Dump a collection from MongoDB."""
    log(f"Dumping collection *{collection.name}* from MongoDB")

    file_path = Path(path) / f"{collection.name}.parquet"
    file_path.parent.mkdir(exist_ok=True)
    data = aggregate_arrow_all(collection, pipeline=pipeline, schema=schema)
    pq.write_table(data, file_path)

    return file_path
