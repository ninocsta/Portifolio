# Setup

```bash
cd /home/nicolas/Documentos/github/Portifolio
./apps/control/scripts/setup_demo_db.sh
./apps/control/scripts/run_demo_server.sh

cd /home/nicolas/Documentos/github/Portifolio/apps/control
npm install
PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers ./node_modules/.bin/playwright install chromium
npm run portfolio:screenshots
```
