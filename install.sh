#!/usr/bin/env bash
set -e
REPO="git@github.com:agaragon/word-counter.git"
VENV_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/word-counter-venv"
BIN_DIR="$HOME/.local/bin"
DIR=$(mktemp -d)
trap 'rm -rf "$DIR"' EXIT

command -v git >/dev/null 2>&1 || { echo "Need git installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Need python3 installed."; exit 1; }

git clone --depth 1 "$REPO" "$DIR"
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --quiet "$DIR"
mkdir -p "$BIN_DIR"
ln -sf "$VENV_DIR/bin/word-counter" "$BIN_DIR/word-counter"

echo "Installed. Run: word-counter --help"
echo "If 'word-counter' is not found, add $BIN_DIR to your PATH."