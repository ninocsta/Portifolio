#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
APP_ROOT="${PORTFOLIO_APP_ROOT:-$(cd "$ROOT_DIR/../loja_carros" && pwd)}"
PYTHON_BIN="$APP_ROOT/venv/bin/python"
DB_PATH="$ROOT_DIR/apps/loja_carros/demo/portfolio.sqlite3"

rm -f "$DB_PATH"
mkdir -p "$(dirname "$DB_PATH")"

export DATABASE_URL="sqlite:///$DB_PATH"
export DEBUG="True"
export ALLOWED_HOSTS="127.0.0.1,localhost,.localtest.me"
export CSRF_TRUSTED_ORIGINS="http://127.0.0.1:8007,http://localhost:8007,http://demo.localtest.me:8007"
export SAAS_BASE_DOMAIN="localtest.me"
export SAAS_NAME="Portfolio Motors Platform"
export PORTFOLIO_APP_ROOT="$APP_ROOT"

cd "$APP_ROOT"
"$PYTHON_BIN" manage.py migrate --noinput
"$PYTHON_BIN" "$ROOT_DIR/apps/loja_carros/scripts/seed_demo.py"
echo "Banco demo pronto em: $DB_PATH"
