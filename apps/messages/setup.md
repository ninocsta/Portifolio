# Como rodar a versão de portfolio

## Pré-requisitos

- repositório `messages/` disponível como irmão do repositório `Portifolio/`
- `./venv/bin/python` funcional dentro de `messages/`
- Node.js e NPM

## Passo a passo

```bash
./apps/messages/scripts/setup_demo_db.sh
./apps/messages/scripts/run_demo_server.sh
```

Em outro terminal:

```bash
cd apps/messages
npm install
PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers npx playwright install chromium
npm run portfolio:screenshots
```
