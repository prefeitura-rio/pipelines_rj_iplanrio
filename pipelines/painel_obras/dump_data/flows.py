# -*- coding: utf-8 -*-
from prefect import Parameter
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_utils.custom import Flow
from prefeitura_rio.pipelines_utils.state_handlers import (
    handler_initialize_sentry,
    handler_inject_bd_credentials,
)
from prefeitura_rio.pipelines_utils.tasks import (
    get_project_id,
    rename_current_flow_run_dataset_table,
)

from pipelines.constants import constants
from pipelines.painel_obras.dump_data.schedules import painel_obras__dump_data_schedule
from pipelines.painel_obras.dump_data.tasks import download_data_to_gcs

with Flow(
    name="IPLANRIO: Painel de obras - Dump to GCS",
    state_handlers=[
        handler_initialize_sentry,
        handler_inject_bd_credentials,
    ],
    parallelism=10,
    skip_if_running=False,
) as rj_iplanrio__painel_obras__dump_data__flow:
    project_id = Parameter("project_id", required=False)
    dataset_id = Parameter("dataset_id")
    table_id = Parameter("table_id")
    query = Parameter("query")
    billing_project_id = Parameter("billing_project_id", required=False)
    bd_project_mode = Parameter("bd_project_mode", required=False, default="prod")

    rename_flow_run = rename_current_flow_run_dataset_table(
        prefix="IPLANRIO: Painel de obras - Dump to GCS: ",
        dataset_id=dataset_id,
        table_id=table_id,
    )

    final_project_id = get_project_id(project_id=project_id, bd_project_mode=bd_project_mode)
    final_project_id.set_upstream(rename_flow_run)

    download_task = download_data_to_gcs(
        project_id=final_project_id,
        dataset_id=dataset_id,
        table_id=table_id,
        query=query,
        bd_project_mode=bd_project_mode,
        billing_project_id=billing_project_id,
    )

rj_iplanrio__painel_obras__dump_data__flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)
rj_iplanrio__painel_obras__dump_data__flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[constants.RJ_IPLANRIO_AGENT_LABEL.value],
)
rj_iplanrio__painel_obras__dump_data__flow.schedule = painel_obras__dump_data_schedule
