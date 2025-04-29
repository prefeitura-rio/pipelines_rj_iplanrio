# -*- coding: utf-8 -*-
from prefect import task
from prefeitura_rio.pipelines_utils.infisical import get_secret
from prefeitura_rio.pipelines_utils.logging import log
import os

DBT_SECRETS = [
    "DBT_BQ_MONITORING_GCP_BIGQUERY_AUDIT_LOGS_TABLE",
    "DBT_BQ_MONITORING_GCP_BILLING_EXPORT_DATASET",
    "DBT_BQ_MONITORING_GCP_BILLING_EXPORT_TABLE"
]


@task
def add_dbt_secrets_to_env():
    """
    Carrega segredos do DBT do Infisical e define como variáveis de ambiente.
    """
    secrets_dict = {}

    for secret_name in DBT_SECRETS:
        try:
            secret = get_secret(secret_name=secret_name, path="/dbt")
            value = secret[secret_name]
            os.environ[secret_name] = value
            secrets_dict[secret_name] = value
            log(f"Variável de ambiente definida: {secret_name}")
        except KeyError:
            log(f"Chave {secret_name} não encontrada no retorno do segredo.")
            raise
        except Exception as e:
            log(f"Erro ao carregar segredo {secret_name}: {e}")
            raise

    return secrets_dict