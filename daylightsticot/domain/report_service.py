import math
from dataclasses import dataclass

from daylightsticot.domain.daylight_client import DaylightClient
from daylightsticot.domain.entities import DaylightReport


@dataclass
class ReportService:
    client: DaylightClient

    def build_report(self) -> DaylightReport:
        raw = self.client.get_report()
        delta = math.floor(
            raw.current_day_report.daylight_duration
            - raw.previous_day_report.daylight_duration
        )
        daylight_duration = math.floor(raw.current_day_report.daylight_duration)
        percent_of_next_solstice = self._compute_percent_of_next_solstice(
            daylight_duration
        )
        return DaylightReport(
            daylight_duration=daylight_duration,
            daylight_delta=delta,
            percent_of_next_solstice=percent_of_next_solstice,
            sunrise_time=raw.current_day_report.sunrise_time,
            sunset_time=raw.current_day_report.sunset_time,
        )

    @staticmethod
    def _compute_percent_of_next_solstice(daylight_duration: int) -> float:
        print(daylight_duration)
        winter_solstice_daylight_duration = 29700
        summer_solstice_daylight_duration = 58200
        return (
            (daylight_duration - winter_solstice_daylight_duration)
            / (summer_solstice_daylight_duration - winter_solstice_daylight_duration)
        ) * 100
