# -*- coding: utf-8 -*-
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

    RJ_IPLANRIO_AGENT_LABEL = "iplanrio"
    SICI_SOAP_API_WSDL = "http://sici.rio.rj.gov.br/Servico/WebServiceSICI.asmx?wsdl"
    TIMEZONE = "America/Sao_Paulo"

    # NEW DBT FLOW
    GCS_BUCKET = {"prod": "rj-iplanrio_dbt", "dev": "rj-iplanrio-dev_dbt"}
    REPOSITORY_URL = "https://github.com/prefeitura-rio/queries-rj-iplanrio.git"
