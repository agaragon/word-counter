"""Command-line interface."""

import argparse
import pathlib
import sys

from word_counter.counter import count_words
from word_counter.dictionary import filter_and_enrich
from word_counter.extractor import extract_text
from word_counter.writer import write_csv


def _process_file(path: pathlib.Path, lang: str, out_path: pathlib.Path, verbose: bool = False, meaning: bool = False) -> bool:
    try:
        text = extract_text(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error {path}: {e}", file=sys.stderr)
        return False
    word_counts = count_words(text)
    if meaning:
        rows = filter_and_enrich(word_counts, lang, verbose=verbose)
    else:
        rows = [(w, c, "") for w, c in word_counts]
    write_csv(rows, out_path, include_meaning=meaning)
    print(f"Wrote {len(rows)} words to {out_path} (from {path.name})")
    return True


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Count word frequencies in .txt or .pdf file(s) and output CSV(s).",
    )
    parser.add_argument(
        "input",
        type=pathlib.Path,
        help="Path to a .txt or .pdf file, or a folder containing such files",
    )
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
        help="Output CSV file (single file) or output directory (when input is a folder)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Log each word (word, count, meaning) to the terminal as it is fetched",
    )
    parser.add_argument(
        "-m",
        "--meaning",
        action="store_true",
        help="Include word meanings in the output CSV",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"Error: {args.input} does not exist", file=sys.stderr)
        sys.exit(1)

    lang = args.language.lower()

    if args.input.is_dir():
        files = sorted(args.input.glob("*.txt")) + sorted(args.input.glob("*.pdf"))
        if not files:
            print(f"No .txt or .pdf files in {args.input}", file=sys.stderr)
            sys.exit(1)
        out_dir = args.input if args.output == pathlib.Path("word_counts.csv") else args.output
        if out_dir.suffix:
            out_dir = out_dir.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        ok = 0
        for path in files:
            if _process_file(path, lang, out_dir / f"{path.stem}.csv", verbose=args.verbose, meaning=args.meaning):
                ok += 1
        if ok < len(files):
            sys.exit(1)
    else:
        if not _process_file(args.input, lang, args.output, verbose=args.verbose, meaning=args.meaning):
            sys.exit(1)
