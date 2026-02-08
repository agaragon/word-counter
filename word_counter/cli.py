"""Command-line interface."""

import argparse
import pathlib
import sys

from word_counter.counter import count_words
from word_counter.dictionary import filter_and_enrich
from word_counter.extractor import extract_text
from word_counter.writer import write_csv


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Count word frequencies in a .txt or .pdf file and output a CSV.",
    )
    parser.add_argument("input", type=pathlib.Path, help="Path to a .txt or .pdf file")
    parser.add_argument(
        "-l",
        "--language",
        required=True,
        metavar="LANG",
        help="Language code of the book (e.g. en, es, fr) for dictionary lookup",
    )
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
    filtered = filter_and_enrich(word_counts, args.language.lower())
    write_csv(filtered, args.output)
    print(f"Wrote {len(filtered)} words to {args.output} (filtered from {len(word_counts)} unique tokens)")
