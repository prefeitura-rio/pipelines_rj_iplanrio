from enum import Enum


class constants(Enum):
    """Constants for the pipelines/taxirio project."""

    DATASET_ID = "transporte_rodoviario_taxirio_staging"
    TABLE_ID = "cities"
    MONGO_CONNECTION = "DB_CONNECTION_STRING"
    RJ_IPLANRIO_TAXIRIO_AGENT_LABEL = "taxirio"
