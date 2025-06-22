#!/bin/bash

echo "🔎 Sherlock Ohms engaged. Commencing symbolic file recovery..."

TARGET="$1"
BASE_DIR="$2"

if [ -z "$TARGET" ]; then
  echo "❌ Please specify a file to search for. Usage: sherlock_ohms.sh evolve.py [/optional/search/root]"
  exit 1
fi

SEARCH_ROOT="${BASE_DIR:-$HOME}"

echo "📍 Searching for: $TARGET"
echo "📂 Starting from: $SEARCH_ROOT"

# Scan the file system
RESULTS=$(find "$SEARCH_ROOT" -type f -name "$TARGET" 2>/dev/null)

if [ -z "$RESULTS" ]; then
  echo "🛑 No results found for $TARGET"
  exit 2
else
  echo "✅ Found the following matches:"
  echo "$RESULTS"

  echo
  echo "🧠 Suggest restoring which version? (type full path or leave blank to cancel)"
  read -r RESTORE_PATH

  if [ -n "$RESTORE_PATH" ] && [ -f "$RESTORE_PATH" ]; then
    DEST_DIR="codex_alchemy/rituals"
    echo "♻️ Restoring $TARGET to $DEST_DIR/"
    cp "$RESTORE_PATH" "$DEST_DIR/"
    echo "✅ $TARGET restored."
  else
    echo "❌ Restore cancelled or invalid path."
  fi
fi

