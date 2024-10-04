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

_alvaras_infra_query = {
    "classificacao": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_CLASSIFICACAO,
                DESCR_CLASSIFICACAO,
                HIS_ATIVO,
                CODIFICACAO
            FROM SIGA.VW_CLASSIFICACAO
        """,
    },
    "documento_tempo": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                SIGLA_DOC,
                DT_PRIMEIRAASSINATURA,
                ULTIMO_ID_MOV,
                DT_FINALIZACAO,
                ARQUIVADO,
                ID_MOBIL,
                TEMPO_TRAMITACAO,
                ID_LOTA_RESP,
                LOTACAO_RESP,
                DATA_COM_RESP_ATUAL
            FROM SIGA.DOCUMENTOS_TEMPO
        """,
    },
    "forma_documento": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_FORMA_DOC,
                DESCR_FORMA_DOC,
                SIGLA_FORMA_DOC,
                ID_TIPO_FORMA_DOC
            FROM SIGA.VW_FORMA_DOCUMENTO
        """,
    },
    "lotacao": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_LOTACAO,
                DATA_INI_LOT,
                DATA_FIM_LOT,
                NOME_LOTACAO,
                ID_LOTACAO_PAI,
                SIGLA_LOTACAO,
                ID_ORGAO_USU,
                IS_EXTERNA_LOTACAO
            FROM CORPORATIVO.VW_LOTACAO
        """,
    },
    "mobil": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_MOBIL,
                ID_DOC
            FROM SIGA.VW_MOBIL
        """,
    },
    "mobil_tipo": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                *
            FROM SIGA.VW_TIPO_MOBIL
        """,
    },
    "modelo": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_MOD,
                NM_MOD,
                DESC_MOD,
                HIS_ID_INI,
                HIS_IDC_INI,
                HIS_IDC_FIM,
                HIS_ATIVO,
                IS_PETICIONAMENTO
            FROM SIGA.VW_MODELO
        """,
    },
    "movimentacao": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "append",
        "partition_columns": "DT_MOV",
        "partition_date_format": "%Y-%m-%d",
        "lower_bound_date": "current_month",
        "execute_query": """
            SELECT
                ID_MOV,
                ID_TP_MOV,
                ID_CADASTRANTE,
                ID_LOTA_CADASTRANTE,
                CAST(CAST(DT_MOV AS VARCHAR(23)) AS DATE) DT_MOV,
                CAST(CAST(DT_FIM_MOV AS VARCHAR(23)) AS DATE) DT_FIM_MOV,
                ID_MOV_REF,
                ID_MOBIL
            FROM SIGA.VW_MOVIMENTACAO
        """,
    },
    "movimentacao_tipo": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                *
            FROM SIGA.VW_TIPO_MOVIMENTACAO
        """,
    },
    "nivel_acesso": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_NIVEL_ACESSO,
                NM_NIVEL_ACESSO
            FROM SIGA.VW_NIVEL_ACESSO
        """,
    },
    "orgao_usuario": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_ORGAO_USU,
                NM_ORGAO_USU,
                SIGLA_ORGAO_USU,
                COD_ORGAO_USU,
                IS_EXTERNO_ORGAO_USU,
                HIS_ATIVO,
                IS_PETICIONAMENTO
            FROM CORPORATIVO.VW_ORGAO_USUARIO
        """,
    },
    "documento": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "append",
        "partition_columns": "DT_DOC",
        "partition_date_format": "%Y-%m-%d",
        "lower_bound_date": "current_month",
        "execute_query": """
            SELECT
                *
            FROM SIGA.VW_DOCUMENTO
        """,
        "dbt_alias": True,
    },
}

alvaras_infra_clocks = generate_dump_db_schedules(
    interval=timedelta(days=1),
    start_date=datetime(2022, 3, 21, 2, 0, tzinfo=pytz.timezone("America/Sao_Paulo")), # noqa
    labels=[
        constants.RJ_IPLANRIO_AGENT_LABEL.value,
    ],
    db_database="DW_BI_ALVARAS",
    db_host="srv000761.infra.rio.gov.br",
    db_port="1521",
    db_type="oracle",
    dataset_id="corporativo",
    infisical_secret_path="/db-alvaras",
    table_parameters=_alvaras_infra_query,
)

alvaras_infra_daily_update_schedule = Schedule(clocks=untuple(alvaras_infra_clocks)) # noqa


