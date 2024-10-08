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

rj_iplanrio_alvaras_flow = deepcopy(dump_sql_flow)
rj_iplanrio_alvaras_flow.state_handlers = [
    handler_inject_bd_credentials,
    handler_initialize_sentry,
]
rj_iplanrio_alvaras_flow.name = "IPLANRIO: Alvaras - Ingerir tabelas de banco SQL"
rj_iplanrio_alvaras_flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio_alvaras_flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[
        constants.RJ_IPLANRIO_AGENT_LABEL.value,  # label do agente
    ],
)

alvaras_default_parameters = {
    "db_database": "DW_BI_ALVARAS",
    "db_host": "srv000144.infra.rio.gov.br",
    "db_port": "1433",
    "db_type": "oracle",
    "dataset_id": "alvaras",
    "vault_secret_path": "db-alvaras",
}

rj_iplanrio_alvaras_flow = set_default_parameters(
    rj_iplanrio_alvaras_flow,
    default_parameters=alvaras_default_parameters,
)

rj_iplanrio_alvaras_flow.schedule = processorio_infra_daily_update_schedule
