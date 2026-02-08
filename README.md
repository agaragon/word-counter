# word-counter

Count word frequencies in `.txt` or `.pdf` files and export them as CSV. Words are looked up in an online dictionary (by language) so the output includes definitions. Useful for building vocabulary lists from books.

## Requirements

- Python 3.10+
- [PyMuPDF](https://pymupdf.readthedocs.io/) (for PDF support)

## Installation

### Option 1: One-line install (recommended)

Download and run the install script:

```bash
curl -sSL https://raw.githubusercontent.com/agaragon/word-counter/master/install.sh | bash
```

If `word-counter` is not found after install, add `~/.local/bin` to your PATH.

### Option 2: Clone and install

```bash
git clone https://github.com/agaragon/word-counter.git
cd word-counter
pip install .
```

Or install in editable mode for development:

```bash
pip install -e .
```

## Usage

```bash
word-counter <input> -l <LANG> [-o output] [-v]
```

- **input** — Path to a `.txt` or `.pdf` file, or a directory of such files.
- **-l, --language** — Language code for dictionary lookup (e.g. `en`, `es`, `fr`).
- **-o, --output** — Output CSV path (default: `word_counts.csv`). For a directory input, use a directory path and one CSV per file is written.
- **-v, --verbose** — Print each word and its meaning as they are fetched.

### Examples

Single file:

```bash
word-counter book.pdf -l en -o book_words.csv
word-counter chapter.txt -l es -o chapter.csv --verbose
```

All PDFs and TXTs in a folder:

```bash
word-counter ./books -l en -o ./output
```

## License

MIT
