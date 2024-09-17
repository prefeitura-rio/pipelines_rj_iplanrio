from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_utils.custom import Flow
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials
from prefeitura_rio.pipelines_utils.tasks import create_table_and_upload_to_gcs

from pipelines.constants import constants as global_constants
from pipelines.taxirio.cities import tasks
from pipelines.taxirio.cities.schedules import every_month
from pipelines.taxirio.constants import constants as local_constants

with Flow(
    name="IPLANRIO: cities - Dump da tabela do MongoDB do TaxiRio",
    state_handlers=[handler_inject_bd_credentials],
    skip_if_running=True,
    parallelism=10,
) as rj_iplanrio_taxirio_cities_flow:
    connection = tasks.get_mongo_connection_string()

    client = tasks.get_mongo_client(connection)

    cities_collection = tasks.get_mongo_collection(
        client,
        local_constants.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value,
        local_constants.TABLE_ID.value,
    )

    data = tasks.get_collection_data(cities_collection)

    dataframe = tasks.convert_to_df(data)

    path = tasks.save_to_csv(dataframe, local_constants.TABLE_ID.value)

    create_table_and_upload_to_gcs(
        data_path=path,
        table_id=local_constants.TABLE_ID.value,
        dataset_id=local_constants.DATASET_ID.value,
        dump_mode="overwrite",
    )

rj_iplanrio_taxirio_cities_flow.storage = GCS(global_constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio_taxirio_cities_flow.schedule = every_month

rj_iplanrio_taxirio_cities_flow.run_config = KubernetesRun(
    image=global_constants.DOCKER_IMAGE.value,
    labels=[local_constants.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
)
