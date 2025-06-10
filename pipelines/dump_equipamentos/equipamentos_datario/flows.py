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
from pipelines.dump_equipamentos.equipamentos_datario.schedules import (
    schedules_equipamentos,
)
from pipelines.dump_equipamentos.equipamentos_datario.tasks import (
    download_equipamentos_from_datario,
)

with Flow(
    name="IPLANRIO: EQUIPAMENTOS FROM DATARIO",
    state_handlers=[
        handler_initialize_sentry,
        handler_inject_bd_credentials,
    ],
    parallelism=10,
    skip_if_running=False,
) as rj_iplanrio__dump_equipamentos_datario__flow:
    url = Parameter(
        "url",
        default="https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Cultura/Equipamentos_SMC/MapServer/0",
        required=True,
    )
    crs = Parameter("crs", default="EPSG:31983", required=True)
    dataset_id = Parameter("dataset_id", default="brutos_equipamentos", required=True)
    table_id = Parameter("table_id", default="culturais", required=True)

    rename_flow_run = rename_current_flow_run_dataset_table(
        prefix="Dump: ",
        dataset_id=dataset_id,
        table_id=table_id,
    )
    path = download_equipamentos_from_datario(url=url, path="/tmp/equipamentos", crs=crs)
    path.set_upstream(rename_flow_run)

    create_table = create_table_and_upload_to_gcs(
        data_path=path,
        dataset_id=dataset_id,
        table_id=table_id,
        dump_mode="overwrite",
        biglake_table=True,
    )
    create_table.set_upstream(path)

# Flow configuration
rj_iplanrio__dump_equipamentos_datario__flow.storage = GCS(Constants.GCS_FLOWS_BUCKET.value)
rj_iplanrio__dump_equipamentos_datario__flow.run_config = KubernetesRun(
    image=Constants.DOCKER_IMAGE.value,
    labels=[Constants.RJ_IPLANRIO_AGENT_LABEL.value],
)
rj_iplanrio__dump_equipamentos_datario__flow.schedule = schedules_equipamentos
