from enum import Enum


class Constants(Enum):
    """Constants for the project."""

    ######################################
    # Automatically managed, please do not
    # change these values
    ######################################
    DOCKER_TAG = "AUTO_REPLACE_DOCKER_TAG"
    DOCKER_IMAGE_NAME = "AUTO_REPLACE_DOCKER_IMAGE"
    DOCKER_IMAGE = f"{DOCKER_IMAGE_NAME}:{DOCKER_TAG}"
    GCS_FLOWS_BUCKET = "datario-public"
    ######################################

    FLOW_DUMP_TO_GCS_NAME = "IPLANRIO: template - Ingerir tabela zipada para GCS"
    FLOW_EXECUTE_DBT_MODEL_NAME = "IPLANRIO: template - Executa DBT model"
    MAX_BYTES_PROCESSED_PER_TABLE = 5 * 1024 * 1024 * 1024
    PREFECT_DEFAULT_PROJECT = "main"
    RJ_IPLANRIO_AGENT_LABEL = "iplanrio"
    SICI_SOAP_API_WSDL = "http://sici.rio.rj.gov.br/Servico/WebServiceSICI.asmx?wsdl"
    TIMEZONE = "America/Sao_Paulo"
    WAIT_FOR_MATERIALIZATION_RETRY_ATTEMPTS = 3
    WAIT_FOR_MATERIALIZATION_RETRY_INTERVAL = 5
