FROM python:3.13-bookworm

RUN pip install poetry

WORKDIR /daylight

COPY poetry.lock pyproject.toml ./
COPY daylightsticot ./daylightsticot/

RUN poetry install

ENTRYPOINT ["poetry", "run", "fastapi", "run", "daylightsticot/endpoints.py"]
