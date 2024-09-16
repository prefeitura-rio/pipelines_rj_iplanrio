from typing import Any

import pandas as pd
from prefect import task
from pymongo.collection import Collection

from pipelines.taxirio.utils import MongoTaxiRio
from pipelines.utils import log

mongo = MongoTaxiRio()
collection = mongo.get_collection("cities")


@task
def get_data(collection: Collection) -> list[dict[str, Any]]:
    """Get data from MongoDB"""
    log("Getting data from MongoDB")
    return list(collection.find())


@task
def convert_to_df(data: list) -> pd.DataFrame:
    """Convert data to DataFrame"""
    log("Converting data to DataFrame")
    return pd.DataFrame(data).drop("_id", axis=1)


@task
def save_to_csv(data: pd.DataFrame) -> None:
    """Save data to Parquet"""
    log("Saving data to Parquet")
    data.to_csv("cities.csv", index=False)
