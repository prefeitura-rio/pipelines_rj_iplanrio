from datetime import datetime, timedelta

from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock
from pytz import timezone

from pipelines.constants import constants
from pipelines.taxirio.constants import Constants as TaxiRio


def every_month(year: int, month: int, day: int) -> Schedule:
    """Every month schedule."""
    return Schedule(
        clocks=[
            IntervalClock(
                interval=timedelta(days=30),
                start_date=datetime(
                    year=year,
                    month=month,
                    day=day,
                    hour=0,
                    minute=0,
                    second=0,
                    tzinfo=timezone(constants.TIMEZONE.value),
                ),
                labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
            ),
        ],
    )


def every_week(year: int, month: int, day: int) -> Schedule:
    """Every week schedule."""
    return Schedule(
        clocks=[
            IntervalClock(
                interval=timedelta(days=7),
                start_date=datetime(
                    year=year,
                    month=month,
                    day=day,
                    hour=0,
                    minute=0,
                    second=0,
                    tzinfo=timezone(constants.TIMEZONE.value),
                ),
                labels=[TaxiRio.RJ_IPLANRIO_TAXIRIO_AGENT_LABEL.value],
            ),
        ],
    )
