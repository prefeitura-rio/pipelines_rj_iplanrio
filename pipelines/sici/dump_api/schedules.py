# -*- coding: utf-8 -*-
# flake8: noqa
from datetime import datetime, timedelta

import pytz
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock

from pipelines.constants import constants

TIMEDELTA_ONCE_A_MONTH = timedelta(minutes=43830)

sici__dump_api__schedule = Schedule(
    clocks=[
        IntervalClock(
            interval=TIMEDELTA_ONCE_A_MONTH,
            start_date=datetime(2024, 8, 12, 18, tzinfo=pytz.timezone("America/Sao_Paulo")),
            labels=[
                constants.RJ_IPLANRIO_AGENT_LABEL.value,
            ],
            parameter_defaults={
                "dataset_id": "unidade_administrativa",
                "table_id": "orgaos",
                "billing_project_id": "rj-iplanrio",
            },
        )
    ]
)
