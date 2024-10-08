"""
Schedules for the database dump pipeline.
"""

from datetime import datetime, timedelta

import pytz
from prefect.schedules import Schedule
from prefeitura_rio.pipelines_utils.io import untuple_clocks as untuple
from prefeitura_rio.pipelines_utils.prefect import generate_dump_db_schedules

from pipelines.constants import constants

#####################################
#
# Alvaras Schedules
#
#####################################

_alvaras_infra_query = {
    "dim_atividade_processo": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT DISTINCT
                        modelo.code [ID_AtvProcesso],
                        modelo.NAME [DSC_AtvProcesso],
                        CASE WHEN modelo.code IN ('_FACCFF13-C8D0-42AC-A64E-A4A0A484BA1A', '_1D641535-BF01-4463-9ED7-2EA98BE86C20',
                                                '_1CE33725-EEFE-49B7-ABC4-02F6BAA05E1A', '_23C3C406-1970-4889-A815-792EB989027F',
                                                '_A0B24915-2A13-4A7D-A0A0-43F55B2B3D8D', '_498B08C5-87E0-49C8-AA31-1F961E40D1C8',
                                                '_9703B4AA-6258-4725-B063-030BCDE277DE', '_A693D497-79A7-4E6B-A146-30126783852E')
                                                THEN 'Atividades do Requerente'
                                                    ELSE 'Atividades da PCRJ'
                                                        END AS [DSC_RespAtividade],
                        modeloDoProcesso.NAME [DSC_RefAtividade]
                        FROM ActivityModel modelo WITH (NOLOCK)
                        INNER JOIN Activity atividade WITH (NOLOCK) ON atividade.model_neoId = modelo.neoId
                        INNER JOIN WFProcess wfprocess WITH (NOLOCK) ON atividade.process_neoId = wfprocess.neoId
                        INNER JOIN ProcessModel modeloDoProcesso WITH (NOLOCK) ON wfprocess.model_neoId = modeloDoProcesso.neoId
                        WHERE modelo.code IS NOT NULL
                        UNION ALL SELECT 'N/A','N/A','N/A','N/A';
        """,
    },
}

alvaras_infra_clocks = generate_dump_db_schedules(
    interval=timedelta(days=1),
    start_date=datetime(2022, 3, 21, 2, 0, tzinfo=pytz.timezone("America/Sao_Paulo")),
    labels=[
        constants.RJ_IPLANRIO_AGENT_LABEL.value,
    ],
    db_database="DW_BI_ALVARAS",
    db_host="srv000144.infra.rio.gov.br",
    db_port="1433",
    db_type="oracle",
    dataset_id="alvaras",
    infisical_secret_path="/db-alvaras",
    table_parameters=_alvaras_infra_query,
)

alvaras_infra_daily_update_schedule = Schedule(clocks=untuple(alvaras_infra_clocks))
