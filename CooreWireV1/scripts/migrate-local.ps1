param(
    [string]$DatabaseUrl = ""
)

$defaultDatabaseUrl = "postgresql://corewire:corewire@localhost:5432/corewire"

if (-not $DatabaseUrl) {
    if ($env:COREWIRE_DATABASE_URL) {
        $DatabaseUrl = $env:COREWIRE_DATABASE_URL
    } elseif ($env:DATABASE_URL) {
        $DatabaseUrl = $env:DATABASE_URL
    } else {
        $DatabaseUrl = $defaultDatabaseUrl
    }
}

$env:PYTHONPATH = "apps/api"
$env:COREWIRE_DATABASE_URL = $DatabaseUrl
$env:DATABASE_URL = $DatabaseUrl
alembic -c apps/api/alembic.ini upgrade head
