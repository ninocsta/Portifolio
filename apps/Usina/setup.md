# Setup

```bash
cd /home/nicolas/Documentos/github/Portifolio
./apps/Usina/scripts/setup_demo_db.sh
./apps/Usina/scripts/run_demo_server.sh

cd /home/nicolas/Documentos/github/Portifolio/apps/Usina
npm install
PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers ./node_modules/.bin/playwright install chromium
npm run portfolio:screenshots
```
