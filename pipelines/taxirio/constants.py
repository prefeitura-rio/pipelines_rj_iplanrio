from enum import Enum


class Constants(Enum):
    """Constants for the TaxiRio project."""

    DATASET_ID = "transporte_rodoviario_taxirio"
    MONGODB_CONNECTION_STRING = "DB_CONNECTION_STRING"
    MONGODB_CONNECTION_STRING_STAGING = "DB_CONNECTION_STRING_STAGING"
    MONGODB_DATABASE_NAME = "taxirio"
    RJ_TAXIRIO_AGENT_LABEL = "taxirio-prod"
    RJ_TAXIRIO_AGENT_LABEL_STAGING = "taxirio-staging"
    STAGING_DATASET_ID = "transporte_rodoviario_taxirio_homologacao"
