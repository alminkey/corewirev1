FROM python:3.12-slim

WORKDIR /app

COPY apps/api /app/apps/api
COPY apps/api/alembic.ini /app/apps/api/alembic.ini

RUN pip install --no-cache-dir \
    alembic>=1.18 \
    fastapi>=0.116 \
    psycopg2-binary>=2.9 \
    pydantic>=2.11 \
    sqlalchemy>=2.0 \
    uvicorn[standard]>=0.35

ENV PYTHONPATH=/app/apps/api

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
