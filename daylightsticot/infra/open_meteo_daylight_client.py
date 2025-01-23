from dataclasses import dataclass
from datetime import date, datetime

import requests
from pydantic import BaseModel

from daylightsticot.domain.daylight_client import DaylightClient
from daylightsticot.domain.entities import RawReport, RawReportDay


class OpenMeteoDaily(BaseModel):
    time: list[date]
    sunrise: list[datetime]
    sunset: list[datetime]
    daylight_duration: list[float]


class OpenMeteoDailyUnits(BaseModel):
    time: str
    daylight_duration: str


class OpenMeteoResponse(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    daily_units: OpenMeteoDailyUnits
    daily: OpenMeteoDaily


@dataclass
class OpenMeteoDaylightClient(DaylightClient):
    def get_report(self) -> RawReport:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=sunrise,sunset,daylight_duration&timezone=Europe%2FBerlin&past_days=1&forecast_days=1"
        )

        open_meteo_response = OpenMeteoResponse.model_validate(response.json())
        return RawReport(
            previous_day_report=RawReportDay(
                daylight_duration=open_meteo_response.daily.daylight_duration[0],
                sunrise_time=open_meteo_response.daily.sunrise[0],
                sunset_time=open_meteo_response.daily.sunset[0],
            ),
            current_day_report=RawReportDay(
                daylight_duration=open_meteo_response.daily.daylight_duration[1],
                sunrise_time=open_meteo_response.daily.sunrise[1],
                sunset_time=open_meteo_response.daily.sunset[1],
            ),
        )
