# -*- coding: utf-8 -*-
"""
Database dumping flows for processo.rio arquivo_virtual.
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

from pipelines.constants import Constants
from pipelines.arquivo_virtual.dump_db.schedules import arquivo_virtual_infra_daily_update_schedule

# arquivo_virtual dump db flow
rj_iplanrio_arquivo_virtual_flow = deepcopy(dump_sql_flow)
rj_iplanrio_arquivo_virtual_flow.state_handlers = [
    handler_inject_bd_credentials,
    handler_initialize_sentry,
]
rj_iplanrio_arquivo_virtual_flow.name = "IPLANRIO: - arquivo_virtual - Ingerir tabelas de banco MYSQL"
rj_iplanrio_arquivo_virtual_flow.storage = GCS(Constants.GCS_FLOWS_BUCKET.value)
rj_iplanrio_arquivo_virtual_flow.run_config = KubernetesRun(
    image=Constants.DOCKER_IMAGE.value,
    labels=[
        Constants.RJ_IPLANRIO_AGENT_LABEL.value,  # label do agente
    ],
)

arquivo_virtual_default_parameters = {
    "db_database": "arquivovirtualprd",     # nome do schema/database MySQL
    "db_host": "10.2.211.17",            # host ou IP do servidor MySQL
    "db_port": "3306",                  # porta padrão do MySQL
    "db_type": "mysql",                 # tipo alterado de oracle para mysql
    "dataset_id": "arquivo_virtual",
    "vault_secret_path": "arquivo_virtual-prod",
}


rj_iplanrio_arquivo_virtual_flow = set_default_parameters(
    rj_iplanrio_arquivo_virtual_flow,
    default_parameters=arquivo_virtual_default_parameters,
)

rj_iplanrio_arquivo_virtual_flow.schedule = arquivo_virtual_infra_daily_update_schedule
