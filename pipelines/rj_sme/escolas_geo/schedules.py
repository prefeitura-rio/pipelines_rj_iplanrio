# -*- coding: utf-8 -*-
# flake8: noqa
from datetime import datetime, timedelta

import pytz
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock

from pipelines.constants import Constants

escolas_geo_schedule = Schedule(
    clocks=[
        IntervalClock(
            interval=timedelta(days=1),
            start_date=datetime(2024, 7, 17, 18, tzinfo=pytz.timezone("America/Sao_Paulo")),
            labels=[
                Constants.RJ_IPLANRIO_AGENT_LABEL.value,
            ],
            parameter_defaults={
                "url": "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Educacao/SME/MapServer/1/query",
                "dataset_id": "brutos_educacao_basica",
                "table_id": "escolas_geolocalizadas",
            },
        )
    ]
)
