import valkey
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from daylightsticot.domain.report_service import ReportService
from daylightsticot.infra.open_meteo_daylight_client import \
    OpenMeteoDaylightClient
from daylightsticot.infra.valkey_cached_client import \
    ValkeyCachedDaylightClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="daylightsticot/templates")
service = ReportService(
        client=ValkeyCachedDaylightClient(
            client=OpenMeteoDaylightClient(),
            cache=valkey.Valkey(host="valkey", port=6379, db=0, decode_responses=True),
        )
    )

@app.get("/", response_class=HTMLResponse)
def display_delta(request: Request):
    report = service.build_report()

    formatted_delta = (
        f"{"+" if report.daylight_delta > 0 else ""}{report.daylight_delta}s"
    )
    return templates.TemplateResponse(
        request=request,
        name="delta.html",
        context={
            "delta": formatted_delta,
            "sunrise": report.sunrise_time.time(),
            "sunset": report.sunset_time.time(),
            "daylight_duration": report.daylight_duration,
            "percent_of_next_solstice": round(report.percent_of_next_solstice, 2),
            "progress_bar_width": report.percent_of_next_solstice * 5,
        },
    )
