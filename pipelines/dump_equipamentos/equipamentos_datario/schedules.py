# -*- coding: utf-8 -*-
# flake8: noqa
from datetime import datetime, timedelta

import pytz
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock

from pipelines.constants import Constants


schedules_parameters = [
    {
        "url": "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Educacao/SME/MapServer/1",
        "crs": "EPSG:31983",
        "dataset_id": "brutos_equipamentos",
        "table_id": "escolas_datario",
    },
    {
        "url": "https://services1.arcgis.com/OlP4dGNtIcnD3RYf/arcgis/rest/services/OSA2/FeatureServer/0",
        "crs": "EPSG:3857",
        "dataset_id": "brutos_equipamentos",
        "table_id": "unidades_saude_datario",
    },
    {
        "url": "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Cultura/Equipamentos_SMC/MapServer/0",
        "crs": "EPSG:31983",
        "dataset_id": "brutos_equipamentos",
        "table_id": "culturais_datario",
    },
]

interval_minutes = 2
start_date = datetime(2024, 7, 17, 18, tzinfo=pytz.timezone("America/Sao_Paulo"))
clocks = []
for count, parameters in enumerate(schedules_parameters):
    clocks.append(
        IntervalClock(
            interval=timedelta(days=1),
            start_date=start_date + timedelta(minutes=interval_minutes * count),
            labels=[
                Constants.RJ_IPLANRIO_AGENT_LABEL.value,
            ],
            parameter_defaults=parameters,
        )
    )


schedules_equipamentos = Schedule(clocks=clocks)
