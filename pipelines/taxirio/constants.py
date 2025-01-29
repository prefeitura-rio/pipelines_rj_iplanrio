# -*- coding: utf-8 -*-
from enum import Enum


class Constants(Enum):
    """Constants for the TaxiRio project."""

    DATASET_ID = "transporte_rodoviario_taxirio"
    MONGODB_CONNECTION_STRING = "DB_CONNECTION_STRING"
    MONGODB_DATABASE_NAME = "taxirio"
    RJ_TAXIRIO_AGENT_LABEL = "taxirio-prod"
