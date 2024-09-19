from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_utils.custom import Flow
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials
from prefeitura_rio.pipelines_utils.tasks import create_table_and_upload_to_gcs

from pipelines.constants import constants
from pipelines.taxirio import tasks
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.discounts.constants import Constants as Discounts
from pipelines.taxirio.schedules import every_month

with Flow(
    name="IPLANRIO: discounts - Dump da tabela do MongoDB do TaxiRio",
    state_handlers=[handler_inject_bd_credentials],
    skip_if_running=True,
    parallelism=10,
) as rj_iplanrio__taxirio__discounts__flow:
    connection = tasks.get_mongo_connection_string()

    client = tasks.get_mongo_client(connection)

    discounts_collection = tasks.get_mongo_collection(
        client,
        TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value,
        Discounts.TABLE_ID.value,
    )

    data = tasks.get_collection_data(discounts_collection)

    dataframe = tasks.convert_to_df(data)

    path = tasks.save_to_csv(
        dataframe,
        Discounts.TABLE_ID.value,
    )

    create_table_and_upload_to_gcs(
        data_path=path,
        table_id=Discounts.TABLE_ID.value,
        dataset_id=TaxiRio.DATASET_ID.value,
        dump_mode="overwrite",
    )

rj_iplanrio__taxirio__discounts__flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__taxirio__discounts__flow.schedule = every_month

rj_iplanrio__taxirio__discounts__flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
)
