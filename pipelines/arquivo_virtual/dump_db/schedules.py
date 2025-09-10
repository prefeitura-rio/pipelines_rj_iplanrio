# -*- coding: utf-8 -*-
"""
Schedules for the database dump pipeline.
"""

from datetime import datetime, timedelta

import pytz
from prefect.schedules import Schedule
from prefeitura_rio.pipelines_utils.io import untuple_clocks as untuple
from prefeitura_rio.pipelines_utils.prefect import generate_dump_db_schedules

from pipelines.constants import Constants

#####################################
#
# Processorio Schedules
#
#####################################

_arquivo_virtual_infra_query = {
    "conjunto_arquivo": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_nivel,
                id_conjuntoArquivo,
                id_conjuntoArquivo_pai,
                st_conjuntoArquivo,
                st_conjuntoArquivo_pai,

            FROM conjunto_arquivo
        """,  # noqa
    },
    "a1_identificacao": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                cd_referencia,
                dt_fim,
                dt_iniModalidade,
                dt_pesquisa,
                ds_titulo,
                id_modalidade,
                id_conjuntoArquivo,
                id_setor
            FROM a1_identificacao
        """,  # noqa
    },
    "a2_contextualizacao": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ds_historiaAdm,
                ds_historiaArq,
                id_NaturezaJuridica,
                id_conjuntoArquivo
            FROM a2_contextualizacao
        """,  # noqa
    },
    "a3_conteudo_estrutura": {  
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ds_incorporacoes,
                ds_avalEliminaTemp,
                ds_ambitoConteudo,
                id_conjuntoArquivo,
                ds_organizacao,
                id_estagioTratamento

            FROM a3_conteudo_estrutura
        """,  # noqa
    },
    "a4_condicoes_acesso": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ds_condicoesReproducao,
                id_conjuntoArquivo, 
                obs_restricao,  
                id_restricao,
                id_tipoRestricao
            FROM a4_condicoes_acesso
        """,  # noqa
    },
    "a5_fontes_relacionada": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ds_existLocalOriginais,
                ds_notasPublicacao,
                ds_unidDescRelacionadas,
                ds_outrosDetentores,
                ds_copiasNaInstituicao,
                id_conjuntoArquivo                  
            FROM a5_fontes_relacionada
        """,  # noqa
    },
    "a6_notas": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ds_notaConservacao,
                id_estadoAcervo,
                ds_notasGerais,
                id_conjuntoArquivo                  
            FROM a6_notas
        """,  # noqa
    },
    "a7_controle": {
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
                ds_datasDesc,
                ds_regrasConvencoes,
                ds_notaArquivistica,
                ds_unidadeCustodiadora
                st_arquivoDigital,
                ds_responsavelDesc,
                id_conjuntoArquivo
            FROM a7_controle
        """,  # noqa
    },
    "condic_idioma": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_idioma,
                id_conjuntoArquivo
            FROM condic_idioma
        """,  # noqa
    },
    "condic_inst": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_condicInst,
                id_conjuntoArquivo,
                id_instPesquisa,
                ds_condicInst
            FROM condic_inst
        """,  # noqa
    },
    "context_produtor": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_produtor,
                nm_produtor,
                dt_morteExtincao,
                dt_nascimentoCriacao,
                id_tipoProdutor,
                id_conjuntoArquivo
            FROM context_produtor
        """,  # noqa
    },
    "dimensao_suporte": {
               "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_conjuntoArquivo,
                id_genero,
                id_especie,
                id_capacidade,
                id_tipoEscala,
                id_formato,
                qt_unidade,
                ds_escala,
                obs,
                id_unidade,
                qt_capacidade
            FROM dimensao_suporte
        """,  # noqa
        "dbt_alias": True,
    },
    "procedencia": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_procedencia,
                nr_geralEntradaProc,
                nr_anoProc,
                nm_procedencia,
                id_formaEntrada,
                id_conjuntoArquivo
            FROM procedencia
        """,  # noqa
        "dbt_alias": True,
    },
    "capacidade_armazena": {
       "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Id_capacidade,
                ds_capacidade
            FROM capacidade_armazena
        """,  # noqa
        "dbt_alias": True,
    },
    "especie": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_especie,
                id_genero,
                nm_especie
            FROM especie
        """,  # noqa
        "dbt_alias": True,
    },
    "estado_acervo": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_estadoAcervo,
                nm_estado
            FROM estado_acervo
        """,  # noqa
        "dbt_alias": True,
    },
    "estagio_tratamento": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_estagioTratamento,
                ds_estagioTratamento
            FROM estagio_tratamento
        """,  # noqa
        "dbt_alias": True,
    },
    "forma_entrada": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_formaEntrada,
                ds_formaEntrada
            FROM forma_entrada
        """,  # noqa
        "dbt_alias": True,
    },
    "formato": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_formato,
                id_genero,
                ds_formato
            FROM formato
        """,  # noqa
        "dbt_alias": True,
    },
    "genero": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_genero,
                nm_genero,
                nr_genero
            FROM genero
        """,  # noqa
        "dbt_alias": True,
    },
    "idioma": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_conjuntoArquivo,
                id_idioma,
                nm_idioma
            FROM idioma
        """,  # noqa
        "dbt_alias": True,
    },
    "instrumento_pesquisa": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_conjuntoArquivo,
                id_genero,
                id_instPesquisa,
                ds_instrumento
            FROM instrumento_pesquisa
        """,  # noqa
        "dbt_alias": True,
    },
    "modalidade": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_modalidade,
                ds_modalidade
            FROM modalidade
        """,  # noqa
        "dbt_alias": True,
    },
    "natureza_juridica": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_NaturezaJuridica,
                ds_natureza
            FROM natureza_juridica
        """,  # noqa
        "dbt_alias": True,
    },
    "nivel": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_nivel,
                ds_nivel,
                nr_nivel
            FROM nivel
        """,  # noqa
        "dbt_alias": True,
    },
    "restricao": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_restricao,
                ds_restricaobasica
            FROM restricao
        """,  # noqa
        "dbt_alias": True,
    },
    "tipo_escala": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_tipoEscala,
                ds_tipoEscala
            FROM tipo_escala
        """,  # noqa
        "dbt_alias": True,
    },
    "tipo_produtor": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_tipoProdutor,
                ds_tipoProdutor
            FROM tipo_produtor
        """,  # noqa
        "dbt_alias": True,
    },
    "tipo_restricao": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_tipoRestricao,
                ds_restricao
            FROM tipo_restricao
        """,  # noqa
        "dbt_alias": True,
    },
    "unidade_medida": {
        "biglake_table": True,
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "materialize_to_datario": False,
        "dump_to_gcs": False,
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_unidade,
                nm_unidade
            FROM unidade_medida
        """,  # noqa
        "dbt_alias": True,
    },
    
}
sicop_infra_clocks = generate_dump_db_schedules(
    interval=timedelta(days=1),
    start_date=datetime(2023, 5, 19, 2, 0, tzinfo=pytz.timezone("America/Sao_Paulo")),
    labels=[
        Constants.RJ_IPLANRIO_AGENT_LABEL.value,
    ],
    db_database="arquivovirtualprd",
    db_host="10.2.211.17",
    db_port="3306",
    db_type="mysql",
    dataset_id="administracao_servicos_publicos",
    infisical_secret_path="/db-sicop",
    table_parameters=_sicop_queries,


}




)

sicop_infra_daily_update_schedule = Schedule(clocks=untuple(sicop_infra_clocks))
