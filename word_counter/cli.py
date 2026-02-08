"""Command-line interface."""

import argparse
import pathlib
import sys

from word_counter.counter import count_words
from word_counter.extractor import extract_text
from word_counter.writer import write_csv


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Count word frequencies in a .txt or .pdf file and output a CSV.",
    )
    parser.add_argument("input", type=pathlib.Path, help="Path to a .txt or .pdf file")
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("word_counts.csv"),
        help="Output CSV filename (default: word_counts.csv)",
    )
    args = parser.parse_args(argv)

    try:
        text = extract_text(args.input)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    word_counts = count_words(text)
    write_csv(word_counts, args.output)
    print(f"Wrote {len(word_counts)} unique words to {args.output}")
