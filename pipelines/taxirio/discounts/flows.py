from prefect import Parameter
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_utils.custom import Flow
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials
from prefeitura_rio.pipelines_utils.tasks import create_table_and_upload_to_gcs

from pipelines.constants import constants
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.discounts.constants import Constants as Discounts
from pipelines.taxirio.discounts.mongodb import pipeline, schema
from pipelines.taxirio.schedules import every_month
from pipelines.taxirio.tasks import (
    dump_collection_from_mongodb,
    get_mongodb_client,
    get_mongodb_collection,
    get_mongodb_connection_string,
)

with Flow(
    name="IPLANRIO: discounts - Dump da tabela do MongoDB do TaxiRio",
    state_handlers=[handler_inject_bd_credentials],
    skip_if_running=True,
    parallelism=1,
) as rj_iplanrio__taxirio__discounts__flow:
    path = Parameter("path", default="output")

    connection = get_mongodb_connection_string()

    client = get_mongodb_client(connection)

    collection = get_mongodb_collection(
        client,
        TaxiRio.MONGODB_DATABASE_NAME.value,
        Discounts.TABLE_ID.value,
    )

    file_path = dump_collection_from_mongodb(
        collection=collection,
        path=path,
        schema=schema,
        pipeline=pipeline,
    )

    create_table_and_upload_to_gcs(
        data_path=file_path,
        table_id=Discounts.TABLE_ID.value,
        dataset_id=TaxiRio.DATASET_ID.value,
        dump_mode="overwrite",
    )

rj_iplanrio__taxirio__discounts__flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__taxirio__discounts__flow.schedule = every_month(2024, 9, 1)

rj_iplanrio__taxirio__discounts__flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
)
