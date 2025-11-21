#!/usr/bin/env bash
set -euo pipefail

# Always work from the repo root even if script is invoked elsewhere.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_PATH="$SCRIPT_DIR/backend/.venv"

if [[ ! -d "$VENV_PATH" ]]; then
  python3 -m venv "$VENV_PATH"
fi

# shellcheck disable=SC1090
source "$VENV_PATH/bin/activate"

pip install -r backend/requirements.txt

python -m backend.dev_llm_smoke_test

uvicorn backend.main:app --reload --port 8000
