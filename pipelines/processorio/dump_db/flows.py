# -*- coding: utf-8 -*-
"""
Database dumping flows for processorio.
"""


from copy import deepcopy

from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_templates.dump_db.flows import flow as dump_sql_flow
from prefeitura_rio.pipelines_utils.prefect import set_default_parameters
from prefeitura_rio.pipelines_utils.state_handlers import (
    handler_initialize_sentry,
    handler_inject_bd_credentials,
)

from pipelines.constants import constants
from pipelines.processorio.dump_db.schedules import (
    processorio_infra_daily_update_schedule,
)

rj_iplanrio_processorio_flow = deepcopy(dump_sql_flow)
rj_iplanrio_processorio_flow.state_handlers = [
    handler_inject_bd_credentials,
    handler_initialize_sentry,
]
rj_iplanrio_processorio_flow.name = "IPLANRIO: processo.rio - Ingerir tabelas de banco SQL"
rj_iplanrio_processorio_flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio_processorio_flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[
        constants.RJ_IPLANRIO_AGENT_LABEL.value,  # label do agente
    ],
    cpu_limit="500m",
    cpu_request="500m",
    memory_limit="2Gi",
    memory_request="2Gi",
)

processorio_default_parameters = {
    "db_database": "DW_BI_PROCESSO_RIO",
    "db_host": "10.2.231.73",
    "db_port": "3306",
    "db_type": "mysql",
    "dataset_id": "adm_processo_interno_processorio",
    "infisical_secret_path": "/db-processorio",
}

rj_iplanrio_processorio_flow = set_default_parameters(
    rj_iplanrio_processorio_flow,
    default_parameters=processorio_default_parameters,
)

rj_iplanrio_processorio_flow.schedule = processorio_infra_daily_update_schedule
