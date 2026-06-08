# Como rodar a versão de portfolio

## Pré-requisitos

- repositório `metalforte/` disponível como irmão do repositório `Portifolio/`
- `./venv/bin/python` funcional dentro de `metalforte/`
- Node.js e NPM

## Passo a passo

```bash
./apps/metalforte/scripts/setup_demo_db.sh
./apps/metalforte/scripts/run_demo_server.sh
```

Em outro terminal:

```bash
cd apps/metalforte
npm install
PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers npx playwright install chromium
npm run portfolio:screenshots
```
