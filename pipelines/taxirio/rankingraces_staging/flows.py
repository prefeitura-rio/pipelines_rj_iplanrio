from copy import deepcopy

from prefect.run_configs import KubernetesRun
from prefeitura_rio.pipelines_utils.prefect import set_default_parameters

from pipelines.constants import constants
from pipelines.taxirio.constants import Constants as TaxiRio
from pipelines.taxirio.rankingraces.flows import rj_iplanrio__taxirio__rankingraces__flow

rj_iplanrio__taxirio__rankingraces__staging__flow = deepcopy(rj_iplanrio__taxirio__rankingraces__flow)

rj_iplanrio__taxirio__rankingraces__staging__flow.name = (
    "IPLANRIO: rankingraces - Dump da tabela do MongoDB do TaxiRio (homologação)"
)

rj_iplanrio__taxirio__rankingraces__staging__flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL_STAGING.value],
)

rj_iplanrio__taxirio__rankingraces__staging__flow = set_default_parameters(
    rj_iplanrio__taxirio__rankingraces__staging__flow,
    default_parameters={
        "path": "output",
        "dataset_id": TaxiRio.STAGING_DATASET_ID.value,
    },
)
