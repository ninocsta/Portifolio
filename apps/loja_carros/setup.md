# Setup

Pre-requisitos:

- repositorios `Portifolio/` e `loja_carros/` como irmaos em `/home/nicolas/Documentos/github/`
- ambiente virtual do projeto em `loja_carros/venv`
- Node.js disponivel para o Playwright

Banco demo:

```bash
cd /home/nicolas/Documentos/github/Portifolio/apps/loja_carros
./scripts/setup_demo_db.sh
```

Servidor demo:

```bash
cd /home/nicolas/Documentos/github/Portifolio/apps/loja_carros
./scripts/run_demo_server.sh
```

URLs principais do ambiente demo:

- publico: `http://demo.localtest.me:8007/estoque/`
- portal: `http://demo.localtest.me:8007/accounts/login/`

Captura de screenshots:

```bash
cd /home/nicolas/Documentos/github/Portifolio/apps/loja_carros
npm install
npx playwright install chromium
npm run portfolio:screenshots
```

Saida esperada:

- banco SQLite demo em `demo/portfolio.sqlite3`
- screenshots em `screenshots/`
