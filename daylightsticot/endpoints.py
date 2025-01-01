import json
import logging
import math
from datetime import date, datetime
from functools import cache
from typing import Optional, Tuple

import requests
import valkey
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from valkey.client import Valkey

app = FastAPI()
templates = Jinja2Templates(directory="daylightsticot/templates")


class OpenMeteoDaily(BaseModel):
    time: list[datetime]
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


@app.get("/", response_class=HTMLResponse)
def display_delta(request: Request):
    delta, cache_hit = get_delta_with_cache()
    formatted_delta = f"{"+" if delta > 0 else ""}{delta}s"
    return templates.TemplateResponse(
        request=request,
        name="delta.html",
        context={"delta": formatted_delta, "cache_hit": cache_hit},
    )


def valkey_connection() -> valkey.Valkey:
    return valkey.Valkey(host="valkey", port=6379, db=0, decode_responses=True)


def set_cache(delta: int) -> None:
    today = date.today().isoformat()
    conn = valkey_connection()
    conn.set(today, delta)


def get_delta_with_cache() -> Tuple[int, bool]:
    from_cache = get_delta_from_cache()
    if from_cache is None:
        delta = get_delta()
        set_cache(delta)
        return delta, False
    else:
        return from_cache, True


def get_delta_from_cache() -> Optional[int]:
    today = date.today().isoformat()
    conn = valkey_connection()
    cache_response = conn.get(today)
    assert isinstance(cache_response, Optional[str])
    if cache_response is None:
        return None
    else:
        return int(cache_response)


def get_delta() -> int:
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude=48.8534&longitude=2.3488&daily=daylight_duration&timezone=Europe%2FBerlin&past_days=1&forecast_days=1"
    )

    open_meteo_response = OpenMeteoResponse.model_validate(response.json())
    return math.floor(
        open_meteo_response.daily.daylight_duration[1]
        - open_meteo_response.daily.daylight_duration[0]
    )
