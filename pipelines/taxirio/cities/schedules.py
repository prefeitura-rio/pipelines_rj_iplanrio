from datetime import datetime, timedelta

from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock
from pytz import timezone

from pipelines.constants import constants as global_constants
from pipelines.taxirio.constants import constants as local_constants

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
                tzinfo=timezone(global_constants.TIMEZONE.value),
            ),
            labels=[local_constants.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
        ),
    ],
)
