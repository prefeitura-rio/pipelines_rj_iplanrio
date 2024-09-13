from prefect import Flow
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS

from pipelines.constants import Constants as global_constants
from pipelines.taxirio.cities.tasks import convert_to_df, get_data, save_to_csv
from pipelines.taxirio.constants import Constants as local_constants
from pipelines.taxirio.utils import MongoTaxiRio

with Flow(
    "IPLANRIO: cities - Dump da tabela do MongoDB do TaxiRio",
) as rj_iplanrio_taxirio_cities_flow:
    mongo = MongoTaxiRio()
    collection = mongo.get_collection("cities")
    data = get_data(collection)
    dataframe = convert_to_df(data)
    save_to_csv(dataframe)

rj_iplanrio_taxirio_cities_flow.storage = GCS(global_constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio_taxirio_cities_flow.run_config = KubernetesRun(
    image=global_constants.DOCKER_IMAGE.value,
    labels=[local_constants.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
)
