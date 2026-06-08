# Scripts auxiliares do portfolio

## 1. Preparar o banco demo

```bash
./apps/avcl/scripts/setup_demo_db.sh
```

Esse script:

- localiza o projeto-fonte em um repositório irmão `../avcl`
- cria um SQLite separado em `apps/avcl/demo/portfolio.sqlite3`
- aplica migrações
- executa `python manage.py seed_portfolio --reset`
- cria o usuário `demo` com senha `Demo@123456`
- ativa branding fictício para uso público

## 2. Subir a aplicação em modo portfolio

```bash
./apps/avcl/scripts/run_demo_server.sh
```

Servidor esperado:

- URL: `http://127.0.0.1:8001`
- login: `demo`
- senha: `Demo@123456`

## 3. Instalar Playwright

Dentro de `apps/avcl/`:

```bash
npm install
npx playwright install chromium
```

## 4. Gerar screenshots

Com o servidor demo já em execução:

```bash
cd apps/avcl
npm run portfolio:screenshots
```

Os arquivos serão salvos em `apps/avcl/screenshots/`.
