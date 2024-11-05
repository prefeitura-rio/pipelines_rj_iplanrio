from prefect import Parameter
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_utils.custom import Flow
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials
from prefeitura_rio.pipelines_utils.tasks import create_table_and_upload_to_gcs

from pipelines.constants import constants
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.schedules import every_week
from pipelines.taxirio.tasks import (
    dump_collection_from_mongodb,
    get_mongodb_client,
    get_mongodb_collection,
    get_mongodb_connection_string,
)
from pipelines.taxirio.users.constants import Constants as Users
from pipelines.taxirio.users.mongodb import pipeline, schema

with Flow(
    name="IPLANRIO: users - Dump da tabela do MongoDB do TaxiRio",
    state_handlers=[handler_inject_bd_credentials],
    skip_if_running=True,
    parallelism=1,
) as rj_iplanrio__taxirio__users__flow:
    path = Parameter("path", default="output")
    dataset_id = Parameter("dataset_id", default=TaxiRio.DATASET_ID.value)
    secret_name = Parameter("secret_name", default=TaxiRio.MONGODB_CONNECTION_STRING.value)

    connection = get_mongodb_connection_string(secret_name)

    client = get_mongodb_client(connection)

    collection = get_mongodb_collection(
        client,
        TaxiRio.MONGODB_DATABASE_NAME.value,
        Users.TABLE_ID.value,
    )

    data_path = dump_collection_from_mongodb(
        collection=collection,
        path=path,
        schema=schema,
        pipeline=pipeline,
        partition_cols=["ano_particao", "mes_particao"],
    )

    create_table_and_upload_to_gcs(
        data_path=data_path,
        dataset_id=dataset_id,
        dump_mode="overwrite",
        source_format="parquet",
        table_id=Users.TABLE_ID.value,
    )

rj_iplanrio__taxirio__users__flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__taxirio__users__flow.schedule = every_week(2024, 9, 2)

rj_iplanrio__taxirio__users__flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
)
