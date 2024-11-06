from copy import deepcopy

from prefect.run_configs import KubernetesRun
from prefeitura_rio.pipelines_utils.prefect import set_default_parameters

from pipelines.constants import Constants
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.users.flows import rj_iplanrio__taxirio__users__flow

rj_iplanrio__taxirio__users__staging__flow = deepcopy(rj_iplanrio__taxirio__users__flow)

rj_iplanrio__taxirio__users__staging__flow.name = "IPLANRIO: users - Dump da tabela do MongoDB do TaxiRio (homologação)"

rj_iplanrio__taxirio__users__staging__flow.run_config = KubernetesRun(
    image=Constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_TAXIRIO_AGENT_LABEL_STAGING.value],
)

rj_iplanrio__taxirio__users__staging__flow = set_default_parameters(
    rj_iplanrio__taxirio__users__staging__flow,
    default_parameters={
        "path": "output",
        "secret_name": TaxiRio.MONGODB_CONNECTION_STRING_STAGING.value,
        "dataset_id": TaxiRio.STAGING_DATASET_ID.value,
    },
)
