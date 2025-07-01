# -*- coding: utf-8 -*-
from copy import deepcopy

from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_templates.dbt_transform.flows import (
    templates__dbt_transform__flow,
)
from prefeitura_rio.pipelines_utils.prefect import set_default_parameters
from prefeitura_rio.pipelines_utils.state_handlers import handler_inject_bd_credentials

from pipelines.constants import Constants
from pipelines.dbt_transform.schedules import (
    dbt_schedules,
)

rj_iplanrio__dbt_transform__flow = deepcopy(templates__dbt_transform__flow)
rj_iplanrio__dbt_transform__flow.state_handlers = [handler_inject_bd_credentials]
rj_iplanrio__dbt_transform__flow.storage = GCS(Constants.GCS_FLOWS_BUCKET.value)

rj_iplanrio__dbt_transform__flow.run_config = KubernetesRun(
    image=Constants.DOCKER_IMAGE.value,
    labels=[Constants.RJ_IPLANRIO_AGENT_LABEL.value],
)

rj_iplanrio__dbt_transform__flow = set_default_parameters(
    rj_iplanrio__dbt_transform__flow,
    default_parameters={
        "github_repo": Constants.REPOSITORY_URL.value,
        "gcs_buckets": Constants.GCS_BUCKET.value,
        "bigquery_project": Constants.RJ_IPLANRIO_AGENT_LABEL.value,
    },
)

rj_iplanrio__dbt_transform__flow.schedule = dbt_schedules

# COMMENT TO TRIGGER..............
