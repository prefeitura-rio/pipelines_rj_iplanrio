from datetime import timedelta

from prefect import Parameter, case
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefect.tasks.prefect import create_flow_run, wait_for_flow_run
from prefeitura_rio.pipelines_utils.custom import Flow
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials
from prefeitura_rio.pipelines_utils.tasks import (
    create_table_and_upload_to_gcs,
    get_current_flow_labels,
    task_run_dbt_model_task,
)

from pipelines.constants import Constants
from pipelines.taxirio.cities.constants import Constants as Cities
from pipelines.taxirio.cities.mongodb import pipeline, schema
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.schedules import every_month
from pipelines.taxirio.tasks import (
    dump_collection_from_mongodb,
    get_mongodb_client,
    get_mongodb_collection,
    get_mongodb_connection_string,
)

with Flow(
    name="IPLANRIO: cities - Dump da tabela do MongoDB do TaxiRio",
    state_handlers=[handler_inject_bd_credentials],
    skip_if_running=True,
    parallelism=1,
) as rj_iplanrio__taxirio__cities__flow:
    path = Parameter("path", default="output")
    secret_name = Parameter("secret_name", default=TaxiRio.MONGODB_CONNECTION_STRING.value)
    dataset_id = Parameter("dataset_id", default=TaxiRio.DATASET_ID.value)
    table_id = Parameter("table_id", default=Cities.TABLE_ID.value)
    materialize_after_dump = Parameter("materialize_after_dump", default=False, required=False)

    connection = get_mongodb_connection_string(secret_name)

    client = get_mongodb_client(connection)

    collection = get_mongodb_collection(
        client,
        TaxiRio.MONGODB_DATABASE_NAME.value,
        table_id,
    )

    data_path = dump_collection_from_mongodb(
        collection=collection,
        path=path,
        schema=schema,
        pipeline=pipeline,
    )

    upload_table = create_table_and_upload_to_gcs(
        data_path=data_path,
        dataset_id=dataset_id,
        dump_mode="overwrite",
        source_format="parquet",
        table_id=table_id,
    )

    with case(materialize_after_dump, True):
        current_flow_labels = get_current_flow_labels()

        run_dbt = task_run_dbt_model_task(
            dataset_id=dataset_id,
            table_id=table_id,
            dbt_alias=True,
        )

        run_dbt.set_upstream(upload_table)

rj_iplanrio__taxirio__cities__flow.storage = GCS(Constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__taxirio__cities__flow.schedule = every_month(2024, 9, 1)

rj_iplanrio__taxirio__cities__flow.run_config = KubernetesRun(
    image=Constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_TAXIRIO_AGENT_LABEL.value],
)
