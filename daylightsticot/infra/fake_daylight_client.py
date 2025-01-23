from dataclasses import dataclass, field

from daylightsticot.domain.daylight_client import DaylightClient
from daylightsticot.domain.entities import RawReport
from tests.factories import raw_report_factory


@dataclass
class FakeDaylightClient(DaylightClient):
    report: RawReport = field(default_factory=raw_report_factory)

    def get_report(self) -> RawReport:
        return self.report
