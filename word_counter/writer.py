"""CSV output writer."""

import csv
import pathlib


def write_csv(
    rows: list[tuple[str, int, str]], output: pathlib.Path
) -> None:
    """Write word, count, and meaning to a CSV file."""
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count", "meaning"])
        writer.writerows(rows)
