# Setup

Repositórios esperados como irmãos:

- `/home/nicolas/Documentos/github/Portifolio`
- `/home/nicolas/Documentos/github/innovaled`

Comandos:

```bash
cd /home/nicolas/Documentos/github/Portifolio
./apps/innovaled/scripts/setup_demo_db.sh
./apps/innovaled/scripts/run_demo_server.sh
cd /home/nicolas/Documentos/github/Portifolio/apps/innovaled
npm install
PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers ./node_modules/.bin/playwright install chromium
npm run portfolio:screenshots
```
