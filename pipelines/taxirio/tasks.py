from pathlib import Path

from prefect import task

from pipelines.taxirio import utils
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.utils import log


@task
def dump_collection_from_mongodb(collection_name: str) -> Path:
    """Dump a collection from MongoDB in batches."""
    with utils.log_dump_collection(collection_name):
        connection = utils.get_mongo_connection_string()

        client = utils.get_mongo_client(connection)

        collection = utils.get_mongo_collection(
            client,
            TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value,
            collection_name,
        )

        data = utils.get_collection_data(collection)

        dataframe = utils.convert_to_df(data)

        return utils.save_to_csv(
            dataframe,
            collection_name,
        )


@task
def dump_collection_from_mongodb_in_batches(
    collection_name: str,
    batch_size: int = 1000,
) -> list[Path]:
    """Dump a collection from MongoDB in batches."""
    with utils.log_dump_collection(collection_name):
        paths = []

        connection = utils.get_mongo_connection_string()

        client = utils.get_mongo_client(connection)

        collection = utils.get_mongo_collection(
            client,
            TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value,
            collection_name,
        )

        data = utils.get_collection_data_in_batches(collection, batch_size)

        for counter, batch in enumerate(data):
            documents = list(batch)

            log(f"Dumping batch {counter} of {collection_name} with {len(documents)} documents")

            dataframe = utils.convert_to_df(documents)

            path = utils.save_to_csv(
                dataframe,
                f"{collection_name}_{counter}",
            )

            log(f"Batch {counter} dumped to {path}")

            paths.append(path)

        return paths
