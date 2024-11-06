import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
from prefect import context
from pyarrow import Table
from pymongo.collection import Collection
from pytz import timezone

from pipelines.constants import Constants


def log(message: str, level: str = "info") -> None:
    """Log a message to prefect logger."""
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    if level not in levels:
        msg = f"Invalid log level: {level}"
        raise ValueError(msg)

    context.logger.log(levels[level], message)


def get_mongodb_date_in_collection(collection: Collection, order: int) -> datetime:
    """Get the smallest or latest date from a MongoDB collection based on sort order."""
    log(f"Getting the {'earliest' if order == 1 else 'latest'} date from *{collection.name}* collection")

    pipeline = [
        {"$sort": {"createdAt": order}},
        {"$limit": 1},
        {"$project": {"date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$createdAt"}}}},
        {"$unset": "_id"},
    ]

    result = list(collection.aggregate(pipeline))

    if not result:
        msg = f"Collection *{collection.name}* is empty"
        raise ValueError(msg)

    return datetime.fromisoformat(result[0]["date"])


def get_date_range(
    start: datetime,
    end: datetime,
    freq: str,
) -> pd.DatetimeIndex:
    """Get a date range between two dates."""
    return pd.date_range(
        start=start,
        end=end,
        freq=freq,
        normalize=True,
        tz=timezone(Constants.TIMEZONE.value),
    )


def write_data_to_disk(
    data: Table,
    root_path: Path,
    collection_name: str,
    partition_cols: list[str] | None,
) -> None:
    """Use this helper function to write data to disk."""
    if partition_cols:
        pq.write_to_dataset(
            table=data,
            root_path=root_path,
            partition_cols=partition_cols,
            basename_template=f"{collection_name}_{{i}}.parquet",
            min_rows_per_group=1000,
            max_rows_per_group=10000,
        )
    else:
        pq.write_table(table=data, where=root_path / f"{collection_name}.parquet")
