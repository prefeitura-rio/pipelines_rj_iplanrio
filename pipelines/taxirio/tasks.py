# -*- coding: utf-8 -*-
from collections.abc import Callable
from datetime import datetime, timedelta
from itertools import pairwise
from pathlib import Path
from typing import Any

from prefect import task
from prefeitura_rio.pipelines_utils.infisical import get_secret
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongoarrow.api import Schema, aggregate_arrow_all
from pytz import UTC

from pipelines import utils


@task(checkpoint=False)
def get_mongodb_connection_string(secret_name: str) -> str:
    """Get MongoDB connection string."""
    utils.log("Getting MongoDB connection string")

    connection = get_secret(
        secret_name=secret_name,
        path="/taxirio",
    )

    return connection[secret_name]


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
def get_dates_for_dump_mode(dump_mode: str, collection: Collection) -> tuple[datetime, datetime]:
    """Get dates based on dump mode."""
    if dump_mode == "overwrite":
        base_start = utils.get_mongodb_date_in_collection(collection, order=1)
        base_end = utils.get_mongodb_date_in_collection(collection, order=-1)
        delta = 30
    else:
        base_start = base_end = datetime.now(UTC)
        delta = 1

    start = utils.normalize_date(base_start) - timedelta(days=delta)
    end = utils.normalize_date(base_end) + timedelta(days=delta)

    return start, end


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
def dump_collection_from_mongodb_per_period(
    collection: Collection,
    path: str,
    generate_pipeline: Callable,
    schema: Schema,
    freq: str,
    start_date: datetime,
    end_date: datetime,
    partition_cols: list[str] | None = None,
) -> Path:
    """Dump a collection from MongoDB per month."""
    utils.log(f"Dumping collection *{collection.name}* from MongoDB")

    root_path = Path(path)
    root_path.mkdir(exist_ok=True)

    utils.log("Generating pipelines for each month")
    dates = utils.get_date_range(
        start=start_date,
        end=end_date,
        freq=freq,
    )

    for start, end in pairwise(dates):
        utils.log(
            "Aggregating data from MongoDB from {} to {}".format(
                start.strftime("%Y-%m-%d"),
                end.strftime("%Y-%m-%d"),
            ),
        )

        data = aggregate_arrow_all(
            collection,
            pipeline=generate_pipeline(start, end),
            schema=schema,
        )

        utils.log("Writing data to disk")
        utils.write_data_to_disk(data, root_path, collection.name, partition_cols)

    return root_path
