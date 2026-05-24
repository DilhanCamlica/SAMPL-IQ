#!/usr/bin/env bash
# Swap Obsidian Graph View preset.
# Doctrine : _meta/graph-presets/README.md

set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PRESETS_DIR="$VAULT_ROOT/_meta/graph-presets/presets"
TARGET="$VAULT_ROOT/.obsidian/graph.json"
CURRENT_FILE="$VAULT_ROOT/_meta/graph-presets/current.txt"

list_presets() {
  echo "Available presets:"
  ls -1 "$PRESETS_DIR" | sed 's/\.json$//' | sed 's/^/  - /'
  if [ -f "$CURRENT_FILE" ]; then
    echo ""
    echo "Currently applied: $(cat "$CURRENT_FILE")"
  fi
}

if [ -z "${1:-}" ]; then
  echo "Usage: bash _meta/graph-presets/swap.sh <preset-name>"
  echo ""
  list_presets
  exit 0
fi

PRESET="$PRESETS_DIR/$1.json"
if [ ! -f "$PRESET" ]; then
  echo "Error: preset '$1' not found at $PRESET"
  echo ""
  list_presets
  exit 1
fi

if ! command -v jq &> /dev/null; then
  echo "Error: jq required. Install with 'brew install jq'."
  exit 1
fi

if [ ! -f "$TARGET" ]; then
  echo "Error: $TARGET not found. Open the Graph View in Obsidian once to create it."
  exit 1
fi

# Backup
cp "$TARGET" "$TARGET.bak"

# Merge: keep physical params from TARGET, override filters/colors from PRESET.
# jq -s '.[0] * .[1]' applies preset on top of current → preset keys win,
# unspecified keys (scale, linkDistance, etc.) preserved from current.
jq -s '.[0] * .[1]' "$TARGET" "$PRESET" > "$TARGET.tmp"
mv "$TARGET.tmp" "$TARGET"

# Track current
echo "$1" > "$CURRENT_FILE"

echo "✓ Applied preset: $1"
echo "  Backup at: $TARGET.bak"
echo "  Reload Obsidian (Cmd+R) to see effect."
