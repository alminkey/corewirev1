FROM python:3.12-slim

WORKDIR /app

COPY apps/api /app/apps/api
COPY apps/api/alembic.ini /app/apps/api/alembic.ini

ENV PYTHONPATH=/app/apps/api

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
