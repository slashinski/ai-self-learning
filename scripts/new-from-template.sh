#!/usr/bin/env bash
# Create a file from a schema template in schemas/.
# Usage: new-from-template.sh [--root modules|skills] <schema-name> <output>
#   default root is modules:  new-from-template.sh test-case module-1/exercise-1/create-prd-tests
#                             -> modules/module-1/exercise-1/create-prd-tests.md
#   skills root:              new-from-template.sh --root skills skill create-prd/SKILL
#                             -> skills/create-prd/SKILL.md
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
root="modules"

if [ "${1:-}" = "--root" ]; then
  root="${2:-}"
  shift 2
fi
case "$root" in modules|skills) ;; *) echo "Root must be modules or skills" >&2; exit 1 ;; esac

if [ $# -ne 2 ]; then
  echo "Usage: $0 [--root modules|skills] <schema-name> <output>" >&2
  exit 1
fi

template="$repo/schemas/$1.md"
output="$repo/$root/$2.md"

[ -f "$template" ] || { echo "Schema not found: $template" >&2; exit 1; }
[ ! -e "$output" ] || { echo "Refusing to overwrite: $output" >&2; exit 1; }

mkdir -p "$(dirname "$output")"
cp "$template" "$output"

echo "Created $output from $template"
