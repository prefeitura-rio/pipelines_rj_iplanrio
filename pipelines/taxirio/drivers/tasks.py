from prefect import task
from prefeitura_rio.pipelines_utils.tasks import create_table_and_upload_to_gcs
from pymongo.cursor import Cursor

from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.drivers.constants import Constants as Drivers
from pipelines.taxirio.tasks import convert_to_df, save_to_csv
from pipelines.utils import log


@task(checkpoint=False)
def iterate_over_mongo_cursor(data: Cursor) -> None:
    """Iterate over a MongoDB cursor and save the data to a CSV file."""
    for count, chunk in enumerate(data):
        log(f"Processing chunk {count}...")
        dataframe = convert_to_df(list(chunk))

        path = save_to_csv(
            dataframe,
            f"{Drivers.TABLE_ID.value}_{count}",
        )

        create_table_and_upload_to_gcs(
            data_path=path,
            table_id=Drivers.TABLE_ID.value,
            dataset_id=TaxiRio.DATASET_ID.value,
            dump_mode="append",
        )

    log("All chunks processed.")
