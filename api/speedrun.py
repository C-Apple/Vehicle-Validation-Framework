import time
from functools import lru_cache
from typing import Any
from urllib.parse import quote

import requests
from fastapi import HTTPException

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "Vehicle-Validation-Framework/1.0 (local speedrun link explorer)"
CACHE_TTL_SECONDS = 15 * 60
MIN_REQUEST_INTERVAL_SECONDS = 1.2
_MAX_LINKS = 24

_last_request_at = 0.0


@lru_cache(maxsize=256)
def _cached_links(page: str, bucket: int) -> tuple[str, ...]:
    del bucket
    global _last_request_at

    elapsed = time.monotonic() - _last_request_at
    if elapsed < MIN_REQUEST_INTERVAL_SECONDS:
        time.sleep(MIN_REQUEST_INTERVAL_SECONDS - elapsed)

    try:
        response = requests.get(
            WIKIPEDIA_API,
            params={
                "action": "query",
                "format": "json",
                "formatversion": "2",
                "prop": "links",
                "titles": page,
                "plnamespace": "0",
                "pllimit": "max",
                "redirects": "1",
            },
            headers={"User-Agent": USER_AGENT},
            timeout=8,
        )
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Unable to fetch Wikipedia links: {exc}") from exc
    finally:
        _last_request_at = time.monotonic()

    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        detail = "Wikipedia is rate limiting link requests. Please wait a moment and try again."
        if retry_after:
            detail = f"{detail} Retry after {retry_after} seconds."
        raise HTTPException(status_code=429, detail=detail)

    if not response.ok:
        raise HTTPException(status_code=502, detail=f"Unable to fetch Wikipedia links: HTTP {response.status_code}")

    payload: dict[str, Any] = response.json()
    pages = payload.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing"):
        raise HTTPException(status_code=404, detail=f"Wikipedia page not found: {page}")

    links = [link["title"] for link in pages[0].get("links", []) if "title" in link]
    return tuple(links[:_MAX_LINKS])


def wikipedia_links(page: str) -> list[dict[str, Any]]:
    normalized = page.strip().replace("_", " ")
    if not normalized:
        raise HTTPException(status_code=400, detail="A Wikipedia page title is required")

    bucket = int(time.time() // CACHE_TTL_SECONDS)
    titles = _cached_links(normalized, bucket)
    return [
        {
            "title": title,
            "url": f"https://en.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}",
            "score": _similarity_score(normalized, title),
        }
        for title in titles
    ]


def _similarity_score(source: str, candidate: str) -> float:
    source_tokens = _tokens(source)
    candidate_tokens = _tokens(candidate)
    if not source_tokens or not candidate_tokens:
        return 0.0

    overlap = len(source_tokens & candidate_tokens) / len(source_tokens | candidate_tokens)
    length_balance = min(len(source), len(candidate)) / max(len(source), len(candidate))
    score = (overlap * 0.65) + (length_balance * 0.35)
    return round(max(0.0, min(score, 1.0)), 2)


def _tokens(value: str) -> set[str]:
    return {token for token in value.lower().replace("_", " ").split() if len(token) > 2}
