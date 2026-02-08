"""CSV output writer."""

import csv
import pathlib


def write_csv(word_counts: list[tuple[str, int]], output: pathlib.Path) -> None:
    """Write word-count pairs to a CSV file with 'word' and 'count' columns."""
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        writer.writerows(word_counts)
