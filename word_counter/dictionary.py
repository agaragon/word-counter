"""Look up words in a language dictionary (Free Dictionary API) and return meaning if valid."""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_BASE = "https://api.dictionaryapi.dev/api/v2/entries"
_CACHE_DIR = Path.home() / ".cache" / "word_counter"


def _cache_path(lang: str) -> Path:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return _CACHE_DIR / f"{lang}.json"


def _load_cache(lang: str) -> dict:
    p = _cache_path(lang)
    if p.exists():
        with p.open(encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_cache(lang: str, cache: dict) -> None:
    with _cache_path(lang).open("w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)


def lookup(word: str, lang: str, cache: dict | None = None) -> str | None:
    """Return the first definition for word in lang, or None if not a valid word.
    Uses and updates cache if provided (in-place).
    """
    if cache is None:
        cache = _load_cache(lang)
    key = word.lower()
    if key in cache:
        return cache[key]
    try:
        req = urllib.request.Request(
            f"{_BASE}/{lang}/{urllib.parse.quote(key)}",
            headers={"User-Agent": "word-counter/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
        cache[key] = meaning
        return meaning
    except (urllib.error.HTTPError, KeyError, IndexError):
        cache[key] = None
        return None
    finally:
        time.sleep(0.15)


def filter_and_enrich(
    word_counts: list[tuple[str, int]], lang: str, *, verbose: bool = False
) -> list[tuple[str, int, str]]:
    """Keep only words that exist in lang and add their first definition."""
    cache = _load_cache(lang)
    result = []
    total = len(word_counts)
    for i, (word, count) in enumerate(word_counts):
        meaning = lookup(word, lang, cache)
        if meaning is not None:
            result.append((word, count, meaning))
            if verbose:
                print(f"{word}\t{count}\t{meaning}", file=sys.stderr)
        processed = i + 1
        if not verbose:
            print(f"\rProcessed {processed}/{total} words, {total - processed} remaining", end="", file=sys.stderr)
    if not verbose:
        print(file=sys.stderr)
    _save_cache(lang, cache)
    return result
