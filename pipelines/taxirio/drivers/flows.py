from prefect import unmapped
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_utils.custom import Flow
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials
from prefeitura_rio.pipelines_utils.tasks import create_table_and_upload_to_gcs

from pipelines.constants import constants
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.drivers.constants import Constants as Drivers
from pipelines.taxirio.schedules import every_month
from pipelines.taxirio.tasks import dump_collection_from_mongodb_in_batches

with Flow(
    name="IPLANRIO: drivers - Dump da tabela do MongoDB do TaxiRio",
    state_handlers=[handler_inject_bd_credentials],
    skip_if_running=True,
    parallelism=10,
) as rj_iplanrio__taxirio__drivers__flow:
    create_table_and_upload_to_gcs.map(
        data_path=dump_collection_from_mongodb_in_batches(Drivers.TABLE_ID.value),
        table_id=unmapped(Drivers.TABLE_ID.value),
        dataset_id=unmapped(TaxiRio.DATASET_ID.value),
        dump_mode=unmapped("append"),
    )

rj_iplanrio__taxirio__drivers__flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__taxirio__drivers__flow.schedule = every_month(2024, 9, 1)

rj_iplanrio__taxirio__drivers__flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
)
