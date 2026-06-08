# Portfolio de Aplicações Web

Repositório de apresentação com estudos de caso, screenshots e documentação de projetos desenvolvidos em diferentes stacks e domínios de negócio.

## Objetivo

Este portfolio reúne aplicações reais organizadas como casos de uso de produto e engenharia. O foco é mostrar amplitude de experiência em sistemas administrativos, financeiros, comunicação automatizada, SaaS multi-tenant e operação comercial, sempre com dados fictícios e ambientes seguros para demonstração.

## Projetos

### AVCL

Sistema administrativo para escolinha esportiva com foco em gestão de turmas, alunos, mensalidades e acompanhamento financeiro.

- Documentação: [apps/avcl/README.md](./apps/avcl/README.md)
- Screenshots: [apps/avcl/screenshots](./apps/avcl/screenshots)

### Messages

Plataforma de comunicação automatizada para aniversários e relacionamento via WhatsApp, com gestão de contatos, modelos de mensagem e histórico de entrega.

- Documentação: [apps/messages/README.md](./apps/messages/README.md)
- Screenshots: [apps/messages/screenshots](./apps/messages/screenshots)

### Metalforte

Sistema web para operação comercial e produtiva de indústria leve, cobrindo orçamentos, pedidos, estoque e indicadores de margem.

- Documentação: [apps/metalforte/README.md](./apps/metalforte/README.md)
- Screenshots: [apps/metalforte/screenshots](./apps/metalforte/screenshots)

### Próximos apps em preparação

- `innovaled`
- `control`
- `Usina`
- `loja_carros`

## Estrutura

```text
Portifolio/
├── README.md
├── .gitignore
└── apps/
    ├── avcl/
    ├── messages/
    └── metalforte/
```

## Padrão adotado

- Cada aplicação fica isolada em `apps/<slug>/`.
- O repositório principal funciona como índice geral do portfolio.
- Cada app mantém sua própria documentação, screenshots e scripts auxiliares.
- Bases demonstrativas são separadas do banco original de cada projeto.
- Dados sensíveis, segredos e integrações reais não entram no repositório.

## Observação

Todos os ambientes demonstrativos deste repositório usam dados fictícios e servem exclusivamente para apresentação profissional.
