"""CSV output writer."""

import csv
import pathlib


def write_csv(
    rows: list[tuple[str, int, str]], output: pathlib.Path, *, include_meaning: bool = False
) -> None:
    """Write word and count to a CSV file; optionally include meaning column."""
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if include_meaning:
            writer.writerow(["word", "count", "meaning"])
            writer.writerows(rows)
        else:
            writer.writerow(["word", "count"])
            writer.writerows((r[0], r[1]) for r in rows)
