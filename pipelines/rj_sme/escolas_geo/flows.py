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
from pipelines.rj_sme.escolas_geo.schedules import escolas_geo_schedule
from pipelines.rj_sme.escolas_geo.tasks import download_and_dump_escolas_geo

with Flow(
    name="SME: DUMP ESCOLAS GEOLOCALIZADAS FROM DATARIO",
    state_handlers=[
        handler_initialize_sentry,
        handler_inject_bd_credentials,
    ],
    parallelism=10,
    skip_if_running=False,
) as rj_iplanrio__escolas_geo__dump_datario__flow:
    url = Parameter("https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Educacao/SME/MapServer/1/query")
    dataset_id = Parameter("brutos_educacao_basica")
    table_id = Parameter("escolas_geolocalizadas")

    rename_flow_run = rename_current_flow_run_dataset_table(
        prefix="Dump Escolas: ",
        dataset_id=dataset_id,
        table_id=table_id,
    )
    path = download_and_dump_escolas_geo(url=url, path="/tmp/escolas_geo")
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
rj_iplanrio__escolas_geo__dump_datario__flow.storage = GCS(Constants.GCS_FLOWS_BUCKET.value)
rj_iplanrio__escolas_geo__dump_datario__flow.run_config = KubernetesRun(
    image=Constants.DOCKER_IMAGE.value,
    labels=[Constants.RJ_IPLANRIO_AGENT_LABEL.value],
)
rj_iplanrio__escolas_geo__dump_datario__flow.schedule = escolas_geo_schedule
