#!/bin/bash
# Ponytail: auto-fix permissions & launch FinMath local server

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Clear macOS quarantine & fix permissions recursively
chmod -R 755 . 2>/dev/null
xattr -cr . 2>/dev/null

if [ "$1" = "--open-files" ]; then
  open [0-9]*.html
  exit 0
fi

python3 main.py
