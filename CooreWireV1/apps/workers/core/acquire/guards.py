from urllib.parse import urlparse


ALLOWED_DOMAINS = {
    "example.com",
    "www.example.com",
    "reuters.com",
    "www.reuters.com",
    "apnews.com",
    "www.apnews.com",
    "corewire.local",
}

BLOCKED_HOSTS = {"127.0.0.1", "localhost", "169.254.169.254", "0.0.0.0"}


def validate_fetch_target(url: str) -> None:
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https targets are allowed")

    if hostname in BLOCKED_HOSTS:
        raise ValueError("Blocked fetch target")

    if hostname not in ALLOWED_DOMAINS:
        raise ValueError("Target domain is not allowlisted")
