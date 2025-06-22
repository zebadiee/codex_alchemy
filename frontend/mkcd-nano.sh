#!/bin/zsh
set +o histexpand  # 🛑 Fix the 'event not found' issue in Zsh

FILE="$1"
TEMPLATE="$2"
TARGET_DIR=$(dirname "$FILE")
TARGET_FILE=$(basename "$FILE")
FULL_PATH="$TARGET_DIR/$TARGET_FILE"

mkdir -p "$TARGET_DIR"

if [ ! -f "$FULL_PATH" ]; then
  case "$TEMPLATE" in
    --tsx)
      echo "export default function Home() {
  return (
    <main>
      <h1>Hello, Codex Alchemy</h1>
    </main>
  );
}" > "$FULL_PATH"
      ;;
    --py)
      echo -e "#!/usr/bin/env python3\nprint('Hello from Python script')" > "$FULL_PATH"
      chmod +x "$FULL_PATH"
      ;;
    --sh)
      echo -e "#!/bin/zsh\necho 'Hello from shell script'" > "$FULL_PATH"
      chmod +x "$FULL_PATH"
      ;;
    --txt)
      echo 'New text file started...' > "$FULL_PATH"
      ;;
    *)
      touch "$FULL_PATH"
      ;;
  esac
fi

cd "$TARGET_DIR" && nano "$TARGET_FILE"

