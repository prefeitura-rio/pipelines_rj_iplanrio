from copy import deepcopy

from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_templates.run_dbt_model.flows import (
    templates__run_dbt_model__flow,
)
from prefeitura_rio.pipelines_utils.prefect import set_default_parameters
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials

from pipelines.constants import Constants

rj_iplanrio__run_dbt_model__flow = deepcopy(templates__run_dbt_model__flow)
rj_iplanrio__run_dbt_model__flow.state_handlers = [handler_inject_bd_credentials]
rj_iplanrio__run_dbt_model__flow.storage = GCS(Constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__run_dbt_model__flow.run_config = KubernetesRun(
    image=Constants.DOCKER_IMAGE.value,
    labels=[Constants.RJ_IPLANRIO_AGENT_LABEL.value],
)

rj_iplanrio__run_dbt_model__flow = set_default_parameters(
    rj_iplanrio__run_dbt_model__flow,
    default_parameters={
        "dataset_id": "dataset_id",
        "table_id": "table_id",
    },
)
