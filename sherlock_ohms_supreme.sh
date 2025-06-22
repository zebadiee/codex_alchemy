#!/bin/bash

# 🕵️ Sherlock Ohms Supreme v2 - Universal AI-Powered Detective Script
# Phase 1: Local Smart Search + Actionable Suggestions

SEARCH_TERM="$1"
ROOT_DIR="/Users/dadhoosband"

if [ -z "$SEARCH_TERM" ]; then
  echo "Usage: ./sherlock_ohms_supreme.sh <search_term>"
  exit 1
fi

# Header
clear
echo "\U1F575 Sherlock Ohms Supreme: Universal Detective Mode Activated"
echo "\U0001F4C2 Scanning from: $ROOT_DIR"
echo "\U0001F4CD Searching for: $SEARCH_TERM"
echo ""

# Find matches
MATCHES=$(find "$ROOT_DIR" -type f -iname "*$SEARCH_TERM*" 2>/dev/null)

if [ -z "$MATCHES" ]; then
  echo "❌ No matches found."
  exit 1
fi

# Show matches
echo "✅ Matches found:"
echo "$MATCHES"
echo ""

# Prompt to act
read -p "\U1F9E0 Type the full path to act on (or leave blank to cancel): " TARGET

if [ -z "$TARGET" ]; then
  echo "❌ Cancelled."
  exit 0
fi

# Offer action options
echo "\U0001F50C What would you like to do with this file?"
select ACTION in "Copy" "Move" "Open" "Inspect Contents" "Cancel"; do
  case $ACTION in
    Copy)
      read -p "♻ Where to copy it to? (full path): " DEST
      cp "$TARGET" "$DEST" && echo "✅ Copied to $DEST" || echo "❌ Copy failed."
      break
      ;;
    Move)
      read -p "♻ Where to move it to? (full path): " DEST
      mv "$TARGET" "$DEST" && echo "✅ Moved to $DEST" || echo "❌ Move failed."
      break
      ;;
    Open)
      open "$TARGET"
      echo "🔓 Opened $TARGET"
      break
      ;;
    "Inspect Contents")
      echo "🔮 Previewing first 50 lines of $TARGET"
      head -n 50 "$TARGET"
      break
      ;;
    Cancel)
      echo "❌ Cancelled."
      break
      ;;
  esac
done

# Optional phase 2 follow-up
echo ""
read -p "\U0001F914 Would you like Sherlock to deduce the next logical action? (y/n): " NEXT
if [[ "$NEXT" == "y" || "$NEXT" == "Y" ]]; then
  echo "\U0001F52E Deducing purpose..."
  # Basic deduction logic
  if [[ "$TARGET" == *enforcer* ]]; then
    echo "✨ This appears to be an Enforcer script. Suggest running: ./run_enforcer.sh"
  elif [[ "$TARGET" == *vault.py* ]]; then
    echo "✨ Vault logic detected. You may want to test: 'vault preserve' or 'vault restore'"
  elif [[ "$TARGET" == *evolve.py* ]]; then
    echo "✨ Glyph evolution detected. Try running: 'codex-alchemy glyph evolve'"
  else
    echo "❓ No specific deduction. Would you like to launch the Codex OS or scan again?"
  fi
fi

echo ""
read -p "\U0001F916 Any more services needed? (y/n): " MORE
if [[ "$MORE" == "y" || "$MORE" == "Y" ]]; then
  echo "\U0001F4E6 Rebooting Sherlock..."
  exec "$0"
else
  echo "\U0001F575 Sherlock Ohms signing off. Case closed."
fi

