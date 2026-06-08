#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
APP_ROOT="${PORTFOLIO_APP_ROOT:-$(cd "$ROOT_DIR/../Usina" && pwd)}"
PYTHON_BIN="$APP_ROOT/venv/bin/python"
DB_PATH="$ROOT_DIR/apps/Usina/demo/portfolio.sqlite3"
PORT="${PORTFOLIO_PORT:-8006}"

export DATABASE_URL="sqlite:///$DB_PATH"
export DEBUG="True"
export ALLOWED_HOSTS="127.0.0.1,localhost"
export PORTFOLIO_APP_ROOT="$APP_ROOT"

cd "$APP_ROOT"
exec "$PYTHON_BIN" manage.py runserver "127.0.0.1:$PORT"
