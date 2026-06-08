#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PORTFOLIO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PORTFOLIO_ROOT="$(cd "$APP_PORTFOLIO_DIR/../.." && pwd)"
APP_ROOT="${PORTFOLIO_APP_ROOT:-$(cd "$PORTFOLIO_ROOT/../messages" && pwd)}"
DB_PATH="$APP_PORTFOLIO_DIR/demo/portfolio.sqlite3"

export DEBUG=True
export SECRET_KEY="portfolio-demo-key"
export ALLOWED_HOSTS="127.0.0.1,localhost"
export DATABASE_URL="sqlite:///$DB_PATH"
export SESSION_COOKIE_SECURE=False
export CSRF_COOKIE_SECURE=False
export CSRF_TRUSTED_ORIGINS="http://127.0.0.1:8002,http://localhost:8002"
export WAHA_HOST="http://localhost:3000"
export WAHA_API_KEY="demo-key"
export WAHA_DEFAULT_SESSION="portfolio-demo"
export REPORT_PHONE_NUMBER="5500000000000"
export EMAIL_HOST="localhost"
export EMAIL_PORT="1025"
export EMAIL_HOST_USER="demo@portfolio.local"
export EMAIL_HOST_PASSWORD="demo"
export DEFAULT_FROM_EMAIL="demo@portfolio.local"

mkdir -p "$APP_PORTFOLIO_DIR/demo"
rm -f "$DB_PATH"
"$APP_ROOT/venv/bin/python" "$APP_ROOT/manage.py" migrate
"$APP_ROOT/venv/bin/python" "$APP_PORTFOLIO_DIR/scripts/seed_demo.py"
echo "Banco demo pronto em: $DB_PATH"
