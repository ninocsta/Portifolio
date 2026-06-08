#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
APP_ROOT="${PORTFOLIO_APP_ROOT:-$(cd "$ROOT_DIR/../loja_carros" && pwd)}"
PYTHON_BIN="$APP_ROOT/venv/bin/python"
DB_PATH="$ROOT_DIR/apps/loja_carros/demo/portfolio.sqlite3"
PORT="${PORTFOLIO_PORT:-8007}"

export DATABASE_URL="sqlite:///$DB_PATH"
export DEBUG="True"
export ALLOWED_HOSTS="127.0.0.1,localhost,.localtest.me"
export CSRF_TRUSTED_ORIGINS="http://127.0.0.1:$PORT,http://localhost:$PORT,http://demo.localtest.me:$PORT"
export SAAS_BASE_DOMAIN="localtest.me"
export SAAS_NAME="Portfolio Motors Platform"
export PORTFOLIO_APP_ROOT="$APP_ROOT"

cd "$APP_ROOT"
exec "$PYTHON_BIN" manage.py runserver "0.0.0.0:$PORT"
