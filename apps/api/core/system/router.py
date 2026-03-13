from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from core.observability.metrics import render_metrics


router = APIRouter()


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def readiness() -> dict[str, str]:
    return {"status": "ready"}


@router.get("/metrics")
def metrics() -> PlainTextResponse:
    return PlainTextResponse(render_metrics())
