FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --no-dev

COPY schemas.py extract.py ./
COPY facturas/ ./facturas/

CMD ["uv", "run", "extract.py"]