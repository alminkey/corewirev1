FROM python:3.12-slim

WORKDIR /app

COPY apps/workers /app/apps/workers

ENV PYTHONPATH=/app/apps/workers

CMD ["python", "apps/workers/main.py"]
