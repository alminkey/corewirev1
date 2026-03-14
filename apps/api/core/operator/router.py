from fastapi import APIRouter, Depends

from core.security.internal_auth import require_internal_token


router = APIRouter(prefix="/operator", tags=["operator"])


@router.post("/commands", dependencies=[Depends(require_internal_token)])
def run_operator_commands(payload: dict) -> dict:
    results = []
    for command in payload.get("commands", []):
        results.append(
            {
                "type": command.get("type"),
                "accepted": True,
                "payload": command.get("payload", {}),
            }
        )

    return {"results": results}
