from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_utils.custom import Flow
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials

from pipelines.constants import constants
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.drivers.constants import Constants as Drivers
from pipelines.taxirio.drivers.tasks import iterate_over_mongo_cursor
from pipelines.taxirio.schedules import every_month
from pipelines.taxirio.tasks import (
    get_collection_data,
    get_mongo_client,
    get_mongo_collection,
    get_mongo_connection_string,
)

with Flow(
    name="IPLANRIO: drivers - Dump da tabela do MongoDB do TaxiRio",
    state_handlers=[handler_inject_bd_credentials],
    skip_if_running=True,
    parallelism=1,
) as rj_iplanrio__taxirio__drivers__flow:
    connection = get_mongo_connection_string()

    client = get_mongo_client(connection)

    drivers_collection = get_mongo_collection(
        client,
        TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value,
        Drivers.TABLE_ID.value,
    )

    data = get_collection_data(drivers_collection, batch=1000)

    iterate_over_mongo_cursor(data)

rj_iplanrio__taxirio__drivers__flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__taxirio__drivers__flow.schedule = every_month

rj_iplanrio__taxirio__drivers__flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
)
