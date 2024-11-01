from enum import Enum


class Constants(Enum):
    """Constants for the TaxiRio project."""

    DATASET_ID = "transporte_rodoviario_taxirio"
    STAGING_DATASET_ID = "transporte_rodoviario_taxirio_homologacao"
    MONGODB_CONNECTION_STRING = "DB_CONNECTION_STRING"
    MONGODB_DATABASE_NAME = "taxirio"
    RJ_IPLANRIO_TAXIRIO_AGENT_LABEL = "taxirio-prod"
    RJ_IPLANRIO_TAXIRIO_AGENT_LABEL_STAGING = "taxirio-staging"
