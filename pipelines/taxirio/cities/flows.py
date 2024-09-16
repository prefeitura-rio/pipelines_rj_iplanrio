from prefect import Flow
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS

from pipelines.constants import constants as global_constants
from pipelines.taxirio.cities import tasks
from pipelines.taxirio.constants import constants as local_constants

with Flow(
    "IPLANRIO: cities - Dump da tabela do MongoDB do TaxiRio",
) as rj_iplanrio_taxirio_cities_flow:
    mongo = tasks.get_mongo_instance()
    data = tasks.get_cities_data(mongo)
    dataframe = tasks.convert_to_df(data)
    tasks.save_to_csv(dataframe)

rj_iplanrio_taxirio_cities_flow.storage = GCS(global_constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio_taxirio_cities_flow.run_config = KubernetesRun(
    image=global_constants.DOCKER_IMAGE.value,
    labels=[local_constants.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
)
