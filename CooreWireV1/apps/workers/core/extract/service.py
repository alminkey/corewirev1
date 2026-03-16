from core.acquire.browser_fetch import fetch_with_browser
from core.acquire.http_fetch import fetch_with_http


def acquire_and_extract(url: str, http_fetch=None, browser_fetch=None):
    http_fetch = http_fetch or fetch_with_http
    browser_fetch = browser_fetch or fetch_with_browser

    try:
        return http_fetch(url)
    except RuntimeError:
        return browser_fetch(url)

