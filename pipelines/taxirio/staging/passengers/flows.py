# -*- coding: utf-8 -*-
from copy import deepcopy

from prefect.run_configs import KubernetesRun
from prefeitura_rio.pipelines_utils.prefect import set_default_parameters

from pipelines.constants import Constants
from pipelines.taxirio.passengers.flows import rj_iplanrio__taxirio__passengers__flow
from pipelines.taxirio.staging.constants import Constants as TaxiRio

rj_iplanrio__taxirio__passengers__staging__flow = deepcopy(rj_iplanrio__taxirio__passengers__flow)

rj_iplanrio__taxirio__passengers__staging__flow.name = (
    "IPLANRIO: passengers - Dump da tabela do MongoDB do TaxiRio (homologação)"
)

rj_iplanrio__taxirio__passengers__staging__flow.run_config = KubernetesRun(
    image=Constants.DOCKER_IMAGE.value,
    labels=[TaxiRio.RJ_TAXIRIO_AGENT_LABEL.value],
)

rj_iplanrio__taxirio__passengers__staging__flow = set_default_parameters(
    rj_iplanrio__taxirio__passengers__staging__flow,
    default_parameters={
        "path": "output",
        "secret_name": TaxiRio.MONGODB_CONNECTION_STRING.value,
        "dataset_id": TaxiRio.DATASET_ID.value,
    },
)
