from fastapi import APIRouter, Depends

from core.operator.service import execute_operator_command
from core.security.internal_auth import require_internal_token


router = APIRouter(prefix="/operator", tags=["operator"])


@router.post("/commands", dependencies=[Depends(require_internal_token)])
def run_operator_commands(payload: dict) -> dict:
    results = []
    for command in payload.get("commands", []):
        results.append(execute_operator_command(command))

    return {"results": results}
