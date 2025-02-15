FROM python:3.13-bookworm

RUN pip install poetry

WORKDIR /daylight

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root 

COPY README.md ./
COPY daylightsticot ./daylightsticot/
COPY static ./static/

RUN poetry install


ENTRYPOINT ["poetry", "run", "fastapi", "run", "daylightsticot/endpoints.py"]
