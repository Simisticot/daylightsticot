from datetime import datetime

from pydantic import BaseModel


class DaylightReport(BaseModel):
    daylight_delta: int
    daylight_duration: int
    sunrise_time: datetime
    sunset_time: datetime
    percent_of_next_solstice: float


class RawReportDay(BaseModel):
    sunrise_time: datetime
    sunset_time: datetime
    daylight_duration: float


class RawReport(BaseModel):
    previous_day_report: RawReportDay
    current_day_report: RawReportDay
