from prefect import Flow
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS

from pipelines.constants import constants as global_constants
from pipelines.taxi_rio.cities.tasks import convert_to_df, get_data, save_to_csv
from pipelines.taxi_rio.constants import constants as local_constants
from pipelines.taxi_rio.utils import MongoTaxiRio

with Flow("IPLANRIO: cities - Dump da tabela do MongoDB do TaxiRio") as flow:
    mongo = MongoTaxiRio()
    collection = mongo.get_collection("cities")
    data = get_data(collection)
    dataframe = convert_to_df(data)
    save_to_csv(dataframe)

flow.storage = GCS(global_constants.GCS_FLOWS_BUCKET.value)

flow.run_config = KubernetesRun(
    image=global_constants.DOCKER_IMAGE.value,
    labels=[local_constants.RJ_TAXI_RIO_AGENT_LABEL.value],
)
