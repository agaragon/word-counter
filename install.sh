#!/usr/bin/env bash
set -e
REPO="git@github.com:agaragon/word-counter.git"
DIR=$(mktemp -d)
trap 'rm -rf "$DIR"' EXIT
command -v git >/dev/null 2>&1 || { echo "Need git installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Need python3 installed."; exit 1; }
git clone --depth 1 "$REPO" "$DIR"
python3 -m pip install --user "$DIR" || python3 -m pip install "$DIR"
echo "Installed. Run: word-counter --help"
echo "If 'word-counter' is not found, add ~/.local/bin to your PATH."
