#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PORTFOLIO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PORTFOLIO_ROOT="$(cd "$APP_PORTFOLIO_DIR/../.." && pwd)"
APP_ROOT="${PORTFOLIO_APP_ROOT:-$(cd "$PORTFOLIO_ROOT/../metalforte" && pwd)}"
DB_PATH="$APP_PORTFOLIO_DIR/demo/portfolio.sqlite3"
STATIC_ROOT="$APP_PORTFOLIO_DIR/demo/staticfiles"

export DEBUG=True
export SECRET_KEY="portfolio-demo-key"
export ALLOWED_HOSTS="127.0.0.1,localhost"
export DATABASE_URL="sqlite:///$DB_PATH"
export SESSION_COOKIE_SECURE=False
export CSRF_COOKIE_SECURE=False
export CSRF_TRUSTED_ORIGINS="http://127.0.0.1:8003,http://localhost:8003"
export STATIC_ROOT="$STATIC_ROOT"

mkdir -p "$APP_PORTFOLIO_DIR/demo"
rm -f "$DB_PATH"
"$APP_ROOT/venv/bin/python" "$APP_ROOT/manage.py" migrate
"$APP_ROOT/venv/bin/python" "$APP_PORTFOLIO_DIR/scripts/seed_demo.py"
echo "Banco demo pronto em: $DB_PATH"
