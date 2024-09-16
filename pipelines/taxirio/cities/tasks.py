from typing import Any

import pandas as pd
from prefect import task
from prefeitura_rio.pipelines_utils.infisical import get_secret
from pymongo import MongoClient
from pymongo.collection import Collection

from pipelines.taxirio.constants import constants
from pipelines.utils import log


@task
def get_mongo_client(connection_string: str) -> MongoClient:
    return MongoClient(connection_string)


@task
def get_mongo_connection_string() -> str:
    connection_string = get_secret(
        secret_name=constants.MONGO_CONNECTION.value,
        path="/taxirio",
    )

    return connection_string[constants.MONGO_CONNECTION.value]


@task
def get_cities_collection(client: MongoClient) -> Collection:
    return client[constants.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value][constants.TABLE_ID.value]


@task
def get_cities_data(cities: Collection) -> list[dict[str, Any]]:
    """Get data from MongoDB."""
    log("Getting data from MongoDB")

    return list(cities.find())


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
