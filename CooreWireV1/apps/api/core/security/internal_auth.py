import os

from fastapi import Header, HTTPException, status


def require_internal_token(x_internal_token: str | None = Header(default=None)) -> None:
    expected_token = os.getenv("COREWIRE_INTERNAL_TOKEN", "corewire-internal-token")
    if x_internal_token != expected_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid internal token",
        )
