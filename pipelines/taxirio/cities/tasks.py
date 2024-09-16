from typing import Any

import pandas as pd
from prefect import task

from pipelines.taxirio.utils import MongoTaxiRio
from pipelines.utils import log


@task
def get_cities_data() -> list[dict[str, Any]]:
    """Get data from MongoDB."""
    log("Getting data from MongoDB")

    mongo = MongoTaxiRio()
    collection = mongo.get_collection("cities")
    return list(collection.find())


@task
def convert_to_df(data: list) -> pd.DataFrame:
    """Convert data to DataFrame."""
    log("Converting data to DataFrame")
    return pd.DataFrame(data).drop("_id", axis=1)


@task
def save_to_csv(dataframe: pd.DataFrame) -> None:
    """Save data to .csv file."""
    log("Saving data to .csv")
    dataframe.to_csv("cities.csv", index=False)
