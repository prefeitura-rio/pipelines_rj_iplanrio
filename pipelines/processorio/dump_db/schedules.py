# -*- coding: utf-8 -*-
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
# Processorio Schedules
#
#####################################

_processorio_infra_query = {
    "dim_data": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                IDDATA,
                DATA,
                DATA_INICIO_SEMANA,
                DATA_FIM_SEMANA,
                NUMERO_DIA_SEMANA,
                NOME_DIA_SEMANA,
                NUMERO_DIA_MES,
                IDSEMANA,
                NUMERO_SEMANA_NO_MES,
                NUMERO_SEMANA_NO_ANO,
                NOME_SEMANA_NO_MES,
                NOME_SEMANA_NO_ANO,
                IDQUINZENA,
                NUMERO_QUINZENA,
                NOME_QUINZENA,
                NOME_QUINZENA_ANO,
                IDMES,
                NUMERO_MES,
                NOME_MES,
                IDTRIMESTRE,
                NOME_TRIMESTRE,
                IDSEMESTRE,
                NOME_SEMESTRE,
                IDANO,
                NOME_ANO,
                IDDIA_UTIL,
                DESC_DIA_UTIL
            FROM
                DW_BI_PROCESSO_RIO.DIM_DATA;
        """,  # noqa
    },
    "dim_setor_orgao": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                IDSETOR,
                IDORGAO,
                SIGLA_ORGAO,
                NOME_ORGAO,
                SIGLA_SETOR,
                NOME_SETOR
            FROM
                DW_BI_PROCESSO_RIO.DIM_SETOR_ORGAO;
        """,  # noqa
    },
    "dim_tipo_evento": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                IDTIPO_EVENTO,
                NOME_EVENTO,
                IDGRUPO_EVENTO,
                NOME_GRUPO_EVENTO
            FROM
                DW_BI_PROCESSO_RIO.DIM_TIPO_EVENTO;
        """,  # noqa
    },
    "dim_documento": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                IDDOCUMENTO,
                NUMERO_DOCUMENTO,
                IDCLASSIFICACAO,
                NOME_CLASSIFICACAO,
                CODIGO_CLASSIFICACAO,
                IDSUBCLASSE,
                NOME_SUBCLASSE,
                IDCLASSE,
                NOME_CLASSE,
                IDASSUNTO,
                NOME_ASSUNTO,
                IDFORMA_DOCUMENTO,
                NOME_FORMA_DOCUMENTO,
                IDTIPO_FORMA_DOCUMENTO,
                NOME_TIPO_FORMA_DOCUMENTO
            FROM
                DW_BI_PROCESSO_RIO.DIM_DOCUMENTO;
        """,  # noqa
    },
    "fato_tramitacao_documento": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                IDACAO,
                IDDOCUMENTO,
                IDSETOR,
                IDTIPO_EVENTO,
                IDDATA_INICIO,
                IDDATA_FIM,
                HORA_REGISTRO_INICIO,
                HORA_REGISTRO_FIM,
                IDDATA_INICIO_CICLO,
                IDDATA_FIM_CICLO,
                DATA_HORA_CARGA,
            FROM
                DW_BI_PROCESSO_RIO.FATO_TRAMITACAO_DOCUMENTO;
        """,  # noqa
    },
}

processorio_infra_clocks = generate_dump_db_schedules(
    interval=timedelta(days=1),
    start_date=datetime(2024, 7, 26, 2, 0, tzinfo=pytz.timezone("America/Sao_Paulo")),
    labels=[
        constants.RJ_IPLANRIO_AGENT_LABEL.value,
    ],
    db_database="DW_BI_PROCESSO_RIO",
    db_host="10.70.6.47",
    db_port="1433",
    db_type="sqlserver",
    dataset_id="adm_processo_interno_processorio",
    infisical_secret_path="/db-processorio",
    table_parameters=_processorio_infra_query,
)

processorio_infra_daily_update_schedule = Schedule(clocks=untuple(processorio_infra_clocks))
