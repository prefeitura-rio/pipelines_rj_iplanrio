from datetime import datetime, timedelta

from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock
from pytz import timezone

from pipelines.constants import constants
from pipelines.taxirio.constants import Constants as TaxiRio

every_month = Schedule(
    clocks=[
        IntervalClock(
            interval=timedelta(days=30),
            start_date=datetime(
                year=2024,
                month=9,
                day=17,
                hour=0,
                minute=0,
                second=0,
                tzinfo=timezone(constants.TIMEZONE.value),
            ),
            labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
        ),
    ],
)
