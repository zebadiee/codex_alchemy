#!/bin/bash

if [ ! -d ".cursor" ]; then
  echo "Copying .cursor/ extension into project root..."
  mkdir -p .cursor
  cp -r adaptive-script-generator/.cursor/* .cursor/
  echo "✅ Cursor extension installed."
else
  echo ".cursor/ already exists. Skipping copy."
fi

echo ""
echo "➡️  Load this in Cursor using:"
echo "   'Extensions: Load from folder' > select .cursor/" 