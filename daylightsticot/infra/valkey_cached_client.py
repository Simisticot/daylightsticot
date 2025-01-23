from dataclasses import dataclass
from datetime import date
from typing import Optional

import valkey

from daylightsticot.domain.daylight_client import DaylightClient
from daylightsticot.domain.entities import RawReport


@dataclass
class ValkeyCachedDaylightClient(DaylightClient):
    client: DaylightClient
    cache: valkey.Valkey

    def from_cache(self) -> Optional[RawReport]:
        today = date.today().isoformat()
        cache_response = self.cache.get(today)
        if cache_response is None:
            return None
        else:
            return RawReport.model_validate_json(cache_response)

    def set_cache(self, report: RawReport) -> None:
        today = date.today().isoformat()
        self.cache.set(today, report.model_dump_json())

    def get_report(self) -> RawReport:
        from_cache = self.from_cache()
        if from_cache is None:
            from_client = self.client.get_report()
            self.set_cache(from_client)
            return from_client
        else:
            return from_cache
