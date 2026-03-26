import os
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "CoreWire API"
    llm_router: str = "openrouter"
    model_profile: str = "balanced"
    openrouter_api_key: str | None = None
    corewire_database_url: str | None = None
    database_url: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        env_values = _load_dotenv()
        return cls(
            app_name=env_values.get("COREWIRE_APP_NAME", "CoreWire API"),
            llm_router=env_values.get("COREWIRE_LLM_ROUTER", "openrouter"),
            model_profile=env_values.get("COREWIRE_MODEL_PROFILE", "balanced"),
            openrouter_api_key=env_values.get("OPENROUTER_API_KEY"),
            corewire_database_url=env_values.get("COREWIRE_DATABASE_URL"),
            database_url=env_values.get("DATABASE_URL"),
        )


def _load_dotenv() -> dict[str, str]:
    values: dict[str, str] = dict(os.environ)
    env_path = Path(__file__).resolve().parents[3] / ".env"
    if not env_path.exists():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values.setdefault(key, value)
    return values

