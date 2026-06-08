# Como rodar a versão de portfolio

## Pré-requisitos

- repositório `avcl/` disponível como irmão do repositório `Portifolio/`
- `./venv/bin/python` funcional dentro de `avcl/`
- Node.js e NPM

## Passo a passo

```bash
./apps/avcl/scripts/setup_demo_db.sh
./apps/avcl/scripts/run_demo_server.sh
```

Em outro terminal:

```bash
cd apps/avcl
npm install
npx playwright install chromium
npm run portfolio:screenshots
```

## Observações

- O banco do portfolio é separado do `db.sqlite3` principal.
- Os dados gerados são 100% fictícios.
- O branding usado nos screenshots também é fictício e neutro.
- Se o código-fonte estiver em outro caminho, exporte `PORTFOLIO_APP_ROOT=/caminho/do/avcl`.
