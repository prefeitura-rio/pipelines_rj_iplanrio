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
    "tab_alvara": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_Alvara,
                DSC_Alvara,
                DSC_Endereco,
                DSC_Bairro,
                DSC_Zoneamento,
                DSC_IRLF,
                DSC_TipoAnalise,
                CAST(DSC_TempoRespDia AS float),
                DSC_StatusIntermediario,
                DSC_StatusCPL,
                CAST(DSC_TempoRespMinuto AS float),
                DSC_TipoAlvara,
                CAST(DSC_TaxaOriginal AS float),
                CAST(DSC_TaxaMulta AS float),
                CAST(DSC_TaxaMora AS float),
                CAST(DSC_TaxaTotal AS float),
                DSC_IsentoTaxa,
                CAST(DSC_Numero AS float),
                DSC_AlvaraLiberado
            FROM DW_BI_ALVARAS.dbo.TAB_ALVARA;
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
    db_host="10.70.15.11",
    db_port="1433",
    db_type="sql_server",
    dataset_id="alvaras",
    infisical_secret_path="/db-alvaras",
    table_parameters=_alvaras_infra_query,
)

alvaras_infra_daily_update_schedule = Schedule(clocks=untuple(alvaras_infra_clocks))
