# Portfolio de Aplicações Web

Repositório de apresentação com estudos de caso, screenshots e documentação de sistemas web desenvolvidos em Django, cobrindo operações administrativas, financeiro, comunicação automatizada, CRM comercial e SaaS multi-tenant.

## Objetivo

Este portfolio organiza projetos reais como estudos de caso técnicos. O foco é facilitar a avaliação de experiência prática em produto, backend, modelagem de dados, automação operacional, dashboards e interfaces de gestão, sempre com dados fictícios e ambientes seguros para demonstração.

## Estudos de caso

### AVCL

Sistema administrativo para escolinha esportiva com foco em turmas, alunos, mensalidades e visão financeira.

- Documentação: [apps/avcl/README.md](./apps/avcl/README.md)
- Screenshots: [apps/avcl/screenshots](./apps/avcl/screenshots)

### Messages

Plataforma de comunicação automatizada via WhatsApp com contatos, templates e histórico de mensagens.

- Documentação: [apps/messages/README.md](./apps/messages/README.md)
- Screenshots: [apps/messages/screenshots](./apps/messages/screenshots)

### Metalforte

Sistema web para operação comercial e produtiva de indústria leve, cobrindo orçamentos, pedidos, estoque e margem.

- Documentação: [apps/metalforte/README.md](./apps/metalforte/README.md)
- Screenshots: [apps/metalforte/screenshots](./apps/metalforte/screenshots)

### Innovaled

Aplicação de gestão comercial para contratos recorrentes, pendências, vídeos instalados e acompanhamento operacional.

- Documentação: [apps/innovaled/README.md](./apps/innovaled/README.md)
- Screenshots: [apps/innovaled/screenshots](./apps/innovaled/screenshots)

### Control

Sistema administrativo para gestão de clientes, contratos, infraestrutura recorrente e cobrança. O recorte do portfolio cobre o lado administrativo e financeiro, sem o módulo `/salao`.

- Documentação: [apps/control/README.md](./apps/control/README.md)
- Screenshots: [apps/control/screenshots](./apps/control/screenshots)

### Usina

Plataforma comercial e operacional com contratos, pagamentos, métricas, mensagens e acompanhamento de vídeos pendentes.

- Documentação: [apps/Usina/README.md](./apps/Usina/README.md)
- Screenshots: [apps/Usina/screenshots](./apps/Usina/screenshots)

### loja_carros

SaaS multi-tenant para lojas de veículos, com vitrine pública por domínio da loja e portal autenticado para operação comercial e financeira.

- Documentação: [apps/loja_carros/README.md](./apps/loja_carros/README.md)
- Screenshots: [apps/loja_carros/screenshots](./apps/loja_carros/screenshots)

## Estrutura

```text
Portifolio/
├── README.md
├── .gitignore
└── apps/
    ├── avcl/
    ├── messages/
    ├── metalforte/
    ├── innovaled/
    ├── control/
    ├── Usina/
    └── loja_carros/
```

## Padrão adotado

- Cada aplicação fica isolada em `apps/<slug>/`.
- Cada estudo de caso tem README, stack, features, setup, screenshots e scripts de ambiente demo.
- Bases demonstrativas usam SQLite separado do banco original de cada projeto.
- Credenciais, segredos, webhooks e dados sensíveis não entram no repositório.
- Screenshots são gerados sobre dados fictícios, com foco em leitura rápida por recrutadores e avaliadores técnicos.

## Observação

Todos os ambientes demonstrativos deste repositório usam dados fictícios e servem exclusivamente para apresentação profissional.
