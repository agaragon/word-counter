"""Word normalization and frequency counting."""

import re
from collections import Counter


def count_words(text: str) -> list[tuple[str, int]]:
    """Count word frequencies and return sorted by count ascending.

    Words are lowercased and stripped of punctuation.
    Empty tokens are discarded.
    """
    words = re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", text.lower())
    words = [w for w in words if any(c.isalpha() for c in w)]
    counts = Counter(words)
    return sorted(counts.items(), key=lambda item: item[1])
