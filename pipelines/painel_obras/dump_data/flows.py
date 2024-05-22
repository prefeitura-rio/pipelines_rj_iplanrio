# -*- coding: utf-8 -*-
from copy import deepcopy

from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_templates.dump_to_gcs.flows import flow as dump_to_gcs_flow
from prefeitura_rio.pipelines_utils.prefect import set_default_parameters
from prefeitura_rio.pipelines_utils.state_handlers import (
    handler_initialize_sentry,
    handler_inject_bd_credentials,
)

from pipelines.constants import constants
from pipelines.painel_obras.dump_data.schedules import painel_obras__dump_data_schedule

rj_iplanrio__painel_obras__dump_data_flow = deepcopy(dump_to_gcs_flow)
rj_iplanrio__painel_obras__dump_data_flow.state_handlers = [
    handler_inject_bd_credentials,
    handler_initialize_sentry,
]
rj_iplanrio__painel_obras__dump_data_flow.name = (
    "IPLANRIO: processo.rio - Ingerir tabelas de banco SQL"
)
rj_iplanrio__painel_obras__dump_data_flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__painel_obras__dump_data_flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[
        constants.RJ_IPLANRIO_AGENT_LABEL.value,  # label do agente
    ],
)

painel_obras__dump_data_default_parameters = {
    "project_id": "rj-iplanrio",
    "dataset_id": "painel_obras",
    # "table_id": "", # set this in schedule
    # "query": "", # set this in schedule
    "billing_project_id": "rj-iplanrio",
}

rj_iplanrio__painel_obras__dump_data_flow = set_default_parameters(
    rj_iplanrio__painel_obras__dump_data_flow,
    default_parameters=painel_obras__dump_data_default_parameters,
)

rj_iplanrio__painel_obras__dump_data_flow.schedule = painel_obras__dump_data_schedule
