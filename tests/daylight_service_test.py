import math

from daylightsticot.domain.report_service import ReportService
from daylightsticot.infra.fake_daylight_client import FakeDaylightClient


def test_percent_of_next_solstice_summer_to_winter() -> None:
    service = ReportService(client=FakeDaylightClient())
    report = service.build_report()
    assert math.floor(report.percent_of_next_solstice) == 4
    assert report.daylight_delta == 1000
