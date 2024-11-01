from prefect import Parameter
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_utils.custom import Flow
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials
from prefeitura_rio.pipelines_utils.tasks import create_table_and_upload_to_gcs

from pipelines.constants import constants
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.rankingraces.constants import Constants as RankingRaces
from pipelines.taxirio.rankingraces.mongodb import generate_pipeline, schema
from pipelines.taxirio.schedules import every_day
from pipelines.taxirio.tasks import (
    dump_collection_from_mongodb_per_month,
    get_dates_for_dump_mode,
    get_mongodb_client,
    get_mongodb_collection,
    get_mongodb_connection_string,
)

with Flow(
    name="IPLANRIO: rankingraces - Dump da tabela do MongoDB do TaxiRio",
    state_handlers=[handler_inject_bd_credentials],
    skip_if_running=True,
    parallelism=1,
) as rj_iplanrio__taxirio__rankingraces__flow:
    path = Parameter("path", default="output")
    freq = Parameter("frequency", default="D")
    dump_mode = Parameter("dump_mode", default="append")
    dataset_id = Parameter("dataset_id", default=TaxiRio.DATASET_ID.value)

    connection = get_mongodb_connection_string()
    client = get_mongodb_client(connection)

    collection = get_mongodb_collection(
        client,
        TaxiRio.MONGODB_DATABASE_NAME.value,
        RankingRaces.TABLE_ID.value,
    )

    start_date, end_date = get_dates_for_dump_mode(dump_mode, collection)

    data_path = dump_collection_from_mongodb_per_month(
        collection=collection,
        path=path,
        generate_pipeline=generate_pipeline,
        schema=schema,
        freq=freq,
        start_date=start_date,
        end_date=end_date,
        partition_cols=["ano_particao", "mes_particao"],
    )

    create_table_and_upload_to_gcs(
        data_path=data_path,
        dataset_id=dataset_id,
        dump_mode=dump_mode,
        source_format="parquet",
        table_id=RankingRaces.TABLE_ID.value,
    )

rj_iplanrio__taxirio__rankingraces__flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__taxirio__rankingraces__flow.schedule = every_day(2024, 10, 10, 1, 0)

rj_iplanrio__taxirio__rankingraces__flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
    memory_request="1Gi",
    memory_limit="2Gi",
)
