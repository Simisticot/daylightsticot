from datetime import datetime

from daylightsticot.domain.entities import (DaylightReport, RawReport,
                                            RawReportDay)


def daylight_report_factory() -> DaylightReport:
    return DaylightReport(
        daylight_delta=100,
        daylight_duration=1000,
        sunrise_time=datetime(year=1, month=1, day=1),
        sunset_time=datetime(year=1, month=1, day=1),
        percent_of_next_solstice=10,
    )


def raw_report_factory() -> RawReport:
    return RawReport(
        previous_day_report=RawReportDay(
            daylight_duration=30000,
            sunrise_time=datetime(year=2025, month=1, day=1, hour=8),
            sunset_time=datetime(year=2025, month=1, day=1, hour=16),
        ),
        current_day_report=RawReportDay(
            daylight_duration=31000,
            sunrise_time=datetime(year=2025, month=1, day=1, hour=8),
            sunset_time=datetime(year=2025, month=1, day=1, hour=16, minute=10),
        ),
    )
