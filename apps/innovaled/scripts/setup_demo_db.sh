#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
APP_ROOT="${PORTFOLIO_APP_ROOT:-$(cd "$ROOT_DIR/../innovaled" && pwd)}"
PYTHON_BIN="$APP_ROOT/venv/bin/python"
DB_PATH="$ROOT_DIR/apps/innovaled/demo/portfolio.sqlite3"

rm -f "$DB_PATH"
mkdir -p "$(dirname "$DB_PATH")"

export DATABASE_URL="sqlite:///$DB_PATH"
export DEBUG="True"
export ALLOWED_HOSTS="127.0.0.1,localhost"
export SESSION_COOKIE_SECURE="False"
export CSRF_COOKIE_SECURE="False"
export CSRF_TRUSTED_ORIGINS="http://127.0.0.1:8004,http://localhost:8004"
export PORTFOLIO_APP_ROOT="$APP_ROOT"

cd "$APP_ROOT"
"$PYTHON_BIN" manage.py migrate --noinput
"$PYTHON_BIN" "$ROOT_DIR/apps/innovaled/scripts/seed_demo.py"
echo "Banco demo pronto em: $DB_PATH"
