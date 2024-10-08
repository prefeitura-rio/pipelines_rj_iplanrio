from collections.abc import Callable
from itertools import pairwise
from pathlib import Path
from typing import Any

from prefect import task
from prefeitura_rio.pipelines_utils.infisical import get_secret
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongoarrow.api import Schema, aggregate_arrow_all

from pipelines import utils
from pipelines.taxirio.constants import Constants


@task(checkpoint=False)
def get_mongodb_connection_string() -> str:
    """Get MongoDB connection string."""
    utils.log("Getting MongoDB connection string")

    connection = get_secret(
        secret_name=Constants.MONGODB_CONNECTION_STRING.value,
        path="/taxirio",
    )

    return connection[Constants.MONGODB_CONNECTION_STRING.value]


@task(checkpoint=False)
def get_mongodb_client(connection: str) -> MongoClient:
    """Get MongoDB client."""
    utils.log("Getting MongoDB client")

    return MongoClient(connection)


@task(checkpoint=False)
def get_mongodb_collection(client: MongoClient, database: str, collection: str) -> Collection:
    """Get MongoDB collection."""
    utils.log("Getting MongoDB collection")

    return client[database][collection]


@task(checkpoint=False)
def dump_collection_from_mongodb(
    collection: Collection,
    path: str,
    schema: Schema,
    pipeline: list[dict[str, Any]],
    partition_cols: list[str] | None = None,
) -> Path:
    """Dump a collection from MongoDB."""
    utils.log(f"Dumping collection *{collection.name}* from MongoDB")

    root_path = Path(path)
    root_path.mkdir(exist_ok=True)

    utils.log("Aggregating data from MongoDB")
    data = aggregate_arrow_all(collection, pipeline=pipeline, schema=schema)

    utils.log("Writing data to disk")
    utils.write_data_to_disk(data, root_path, collection.name, partition_cols)

    return root_path


@task(checkpoint=False)
def dump_collection_from_mongodb_per_month(
    collection: Collection,
    path: str,
    generate_pipeline: Callable,
    schema: Schema,
    freq: str,
    partition_cols: list[str] | None = None,
) -> Path:
    """Dump a collection from MongoDB per month."""
    utils.log(f"Dumping collection *{collection.name}* from MongoDB")

    root_path = Path(path)
    root_path.mkdir(exist_ok=True)

    start = utils.get_mongodb_earliest_date_in_collection(collection)
    end = utils.get_mongodb_latest_date_in_collection(collection)

    utils.log("Generating pipelines for each month")
    dates = utils.get_date_range(start=start, end=end, freq=freq)
    pipelines = [generate_pipeline(start, end) for start, end in pairwise(dates)]

    for pipeline in pipelines:
        utils.log("Aggregating data from MongoDB")
        data = aggregate_arrow_all(collection, pipeline=pipeline, schema=schema)

        utils.log("Writing data to disk")
        utils.write_data_to_disk(data, root_path, collection.name, partition_cols)

    return root_path
