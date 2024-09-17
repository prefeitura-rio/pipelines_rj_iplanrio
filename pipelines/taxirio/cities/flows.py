from prefect import Flow
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS

from pipelines.constants import constants as global_constants
from pipelines.taxirio.cities import tasks
from pipelines.taxirio.constants import constants as local_constants

with Flow(
    "IPLANRIO: cities - Dump da tabela do MongoDB do TaxiRio",
) as rj_iplanrio_taxirio_cities_flow:
    connection = tasks.get_mongo_connection_string()

    client = tasks.get_mongo_client(connection)

    data = tasks.get_mongo_collection(
        client,
        local_constants.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value,
        local_constants.TABLE_ID.value,
    )

    data = tasks.get_collection_data(data)

    dataframe = tasks.convert_to_df(data)

    tasks.save_to_csv(dataframe)

rj_iplanrio_taxirio_cities_flow.storage = GCS(global_constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio_taxirio_cities_flow.run_config = KubernetesRun(
    image=global_constants.DOCKER_IMAGE.value,
    labels=[local_constants.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
)
