#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PORTFOLIO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PORTFOLIO_ROOT="$(cd "$APP_PORTFOLIO_DIR/../.." && pwd)"
APP_ROOT="${PORTFOLIO_APP_ROOT:-$(cd "$PORTFOLIO_ROOT/../avcl" && pwd)}"
DB_PATH="$APP_PORTFOLIO_DIR/demo/portfolio.sqlite3"

export DEBUG=True
export SECRET_KEY="portfolio-demo-key"
export ALLOWED_HOSTS="127.0.0.1,localhost"
export DATABASE_URL="sqlite:///$DB_PATH"
export SESSION_COOKIE_SECURE=False
export CSRF_COOKIE_SECURE=False
export CSRF_TRUSTED_ORIGINS="http://127.0.0.1:8001,http://localhost:8001"
export SITE_NAME="Centro Aurora Futsal - Gestao Escolar"
export SITE_SHORT_NAME="CAF"
export SITE_FOOTER_NAME="Portfolio Demo"
export SITE_FOOTER_URL="https://example.invalid"
export SITE_PAYMENT_LABEL="Pix"
export SITE_PAYMENT_KEY="demo-chave-pix-0001"
export SITE_PAYMENT_RECIPIENT="Centro Aurora Futsal"

if [ ! -x "$APP_ROOT/venv/bin/python" ]; then
  echo "Python do projeto nao encontrado em: $APP_ROOT/venv/bin/python" >&2
  exit 1
fi

mkdir -p "$APP_PORTFOLIO_DIR/demo"

"$APP_ROOT/venv/bin/python" "$APP_ROOT/manage.py" migrate
"$APP_ROOT/venv/bin/python" "$APP_ROOT/manage.py" seed_portfolio --reset

echo "Banco demo pronto em: $DB_PATH"
