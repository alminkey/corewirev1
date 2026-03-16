import os

from fastapi import Header, HTTPException, status


def require_owner_token(x_owner_token: str | None = Header(default=None)) -> None:
    expected_token = os.getenv("COREWIRE_OWNER_TOKEN", "corewire-owner-token")
    if x_owner_token != expected_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid owner token",
        )
