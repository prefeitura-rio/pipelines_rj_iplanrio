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
    create_table_and_upload_to_gcs,
    rename_current_flow_run_dataset_table,
)

from pipelines.constants import Constants
from pipelines.sici.dump_api.schedules import sici_dump_api_schedule
from pipelines.sici.dump_api.tasks import (
    get_data_from_api_soap_sici,
    get_sici_api_credentials,
)

with Flow(
    name="IPLANRIO: SICI API - Dump to GCS",
    state_handlers=[
        handler_initialize_sentry,
        handler_inject_bd_credentials,
    ],
    parallelism=10,
    skip_if_running=False,
) as rj_iplanrio__sici__dump_api__flow:
    dataset_id = Parameter("dataset_id")
    table_id = Parameter("table_id")
    billing_project_id = Parameter("billing_project_id", required=False)
    bd_project_mode = Parameter("bd_project_mode", required=False, default="prod")

    rename_flow_run = rename_current_flow_run_dataset_table(
        prefix="Dump SICI API: ",
        dataset_id=dataset_id,
        table_id=table_id,
    )

    get_credentials = get_sici_api_credentials()
    get_credentials.set_upstream(rename_flow_run)

    path = get_data_from_api_soap_sici(
        wsdl=Constants.SICI_SOAP_API_WSDL.value,
        params=get_credentials,
    )

    path.set_upstream(get_credentials)

    create_table = create_table_and_upload_to_gcs(
        data_path=path,
        dataset_id=dataset_id,
        table_id=table_id,
        dump_mode="overwrite",
        biglake_table=True,
    )
    create_table.set_upstream(path)

# Flow configuration
rj_iplanrio__sici__dump_api__flow.storage = GCS(Constants.GCS_FLOWS_BUCKET.value)
rj_iplanrio__sici__dump_api__flow.run_config = KubernetesRun(
    image=Constants.DOCKER_IMAGE.value,
    labels=[Constants.RJ_IPLANRIO_AGENT_LABEL.value],
)
rj_iplanrio__sici__dump_api__flow.schedule = sici_dump_api_schedule
