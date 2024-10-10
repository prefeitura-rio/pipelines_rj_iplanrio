from prefect import Parameter
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_utils.custom import Flow
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials
from prefeitura_rio.pipelines_utils.tasks import create_table_and_upload_to_gcs

from pipelines.constants import constants
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.passengers.constants import Constants as Passengers
from pipelines.taxirio.passengers.mongodb import generate_pipeline, schema
from pipelines.taxirio.schedules import every_week
from pipelines.taxirio.tasks import (
    dump_collection_from_mongodb_per_month,
    get_mongodb_client,
    get_mongodb_collection,
    get_mongodb_connection_string,
)

with Flow(
    name="IPLANRIO: passengers - Dump da tabela do MongoDB do TaxiRio",
    state_handlers=[handler_inject_bd_credentials],
    skip_if_running=True,
    parallelism=1,
) as rj_iplanrio__taxirio__passengers__flow:
    path = Parameter("path", default="output")
    frequency = Parameter("frequency", default="2M")

    connection = get_mongodb_connection_string()

    client = get_mongodb_client(connection)

    collection = get_mongodb_collection(
        client,
        TaxiRio.MONGODB_DATABASE_NAME.value,
        Passengers.TABLE_ID.value,
    )

    data_path = dump_collection_from_mongodb_per_month(
        collection=collection,
        path=path,
        schema=schema,
        freq=frequency,
        generate_pipeline=generate_pipeline,
        partition_cols=["ano_particao", "mes_particao"],
    )

    create_table_and_upload_to_gcs(
        data_path=data_path,
        dataset_id=TaxiRio.DATASET_ID.value,
        dump_mode="overwrite",
        source_format="parquet",
        table_id=Passengers.TABLE_ID.value,
    )

rj_iplanrio__taxirio__passengers__flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__taxirio__passengers__flow.schedule = every_week(2024, 9, 3)

rj_iplanrio__taxirio__passengers__flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
    memory_request="1Gi",
    memory_limit="2Gi",
)
