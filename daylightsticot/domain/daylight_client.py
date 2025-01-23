from abc import abstractmethod
from typing import Protocol

from daylightsticot.domain.entities import RawReport


class DaylightClient(Protocol):
    @abstractmethod
    def get_report(self) -> RawReport: ...
