param(
    [string]$DatabaseUrl = "sqlite:///corewire-local.db"
)

$env:PYTHONPATH = "apps/api"
$env:COREWIRE_DATABASE_URL = $DatabaseUrl
alembic -c apps/api/alembic.ini upgrade head
