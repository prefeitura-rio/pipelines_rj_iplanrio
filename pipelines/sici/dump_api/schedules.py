# -*- coding: utf-8 -*-
# flake8: noqa
from datetime import datetime, timedelta

import pytz
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock

from pipelines.constants import constants



parameter_list = [
    {
        "dataset_id": "unidades_administrativas",
        "table_id": "detalhes",
        "endpoint": "Get_UG_Tipo_UG",
        "endpoint_parameters": {
            "Id_Base": "",
            "Codigo_UG": "",
            "Data_Inicio": "",
            "Data_Fim": "",
            "Tipo_UG": "",
        },
        "billing_project_id": "rj-iplanrio",
        "materialize_after_dump": False,
    },
    {
        "dataset_id": "unidades_administrativas",
        "table_id": "orgaos",
        "endpoint": "Get_Arvore_UA",
        "endpoint_parameters": {
            "Codigo_UA": "",
            "Nivel": "",
            "Tipo_Arvore": "",
        },
        "billing_project_id": "iplanrio",
        "materialize_after_dump": True,
    },
    # Add more parameter dicts as needed
]

sici_dump_api_schedule = Schedule(
    clocks=[
        IntervalClock(
            interval=timedelta(days=1),
            start_date=datetime(2024, 7, 17, 18, tzinfo=pytz.timezone("America/Sao_Paulo")),
            labels=[
                constants.RJ_IPLANRIO_AGENT_LABEL.value,
            ],
            parameter_defaults=params,
        )
        for params in parameter_list
    ]
)
