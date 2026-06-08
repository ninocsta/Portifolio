# Portfolio de Engenharia de Software

Coleção de estudos de caso de sistemas web desenvolvidos em Django, organizados para leitura rápida por recrutadores, líderes técnicos e gestores de produto.

O objetivo deste repositório é mostrar experiência prática em construção de software de negócio: modelagem de domínio, CRUDs operacionais, dashboards, automação, autenticação, cobrança, interfaces administrativas e SaaS multi-tenant.

## Leitura rápida

Se você quiser avaliar este portfolio em poucos minutos:

1. Abra os estudos de caso em [`apps/README.md`](./apps/README.md).
2. Comece por `loja_carros`, `control` ou `avcl`, que mostram bem produto, operação e interface.
3. Em cada app, veja primeiro o `README.md` e depois a pasta `screenshots/`.

## O que este portfolio demonstra

- Backend web com Django em contextos administrativos e comerciais.
- Modelagem de dados orientada a operação real.
- Dashboards e relatórios para leitura gerencial.
- Automações de cobrança, comunicação e recorrência.
- Aplicações multiusuário e, em um caso, multi-tenant por domínio.
- Capacidade de transformar sistemas internos em material apresentável para avaliação técnica.

## Estudos de caso

| Estudo | Domínio | O que evidencia | Link |
|---|---|---|---|
| Gestão esportiva | Escolinha esportiva | alunos, turmas, mensalidades, dashboard financeiro | [`apps/avcl`](./apps/avcl) |
| Messages | Comunicação automatizada | contatos, templates, histórico e status de mensagens | [`apps/messages`](./apps/messages) |
| Operação industrial leve | Produção e comercial | pedidos, orçamentos, estoque e margem | [`apps/metalforte`](./apps/metalforte) |
| Gestão comercial recorrente | Contratos e acompanhamento | contratos, pendências, registros e vídeos | [`apps/innovaled`](./apps/innovaled) |
| Control | Gestão administrativa e financeira | clientes, contratos, invoices e infraestrutura recorrente | [`apps/control`](./apps/control) |
| Operação comercial com mídia | Comercial e execução | contratos, parcelas, métricas e pipeline de vídeos | [`apps/Usina`](./apps/Usina) |
| loja_carros | SaaS multi-tenant | vitrine pública, portal autenticado, billing e operação da loja | [`apps/loja_carros`](./apps/loja_carros) |

## Como cada caso está organizado

Cada pasta em `apps/<slug>/` segue o mesmo padrão:

- `README.md`: resumo executivo do sistema.
- `stack.md`: stack e decisões técnicas principais.
- `features.md`: visão funcional objetiva.
- `setup.md`: como subir o ambiente demo.
- `screenshots/`: telas representativas para avaliação rápida.
- `scripts/`: preparação do banco demo, servidor local e captura.

## Organização do workspace

```text
Portifolio/
├── README.md
├── apps/
│   ├── README.md
│   └── <estudo-de-caso>/
│       ├── README.md
│       ├── stack.md
│       ├── features.md
│       ├── setup.md
│       ├── screenshots/
│       └── scripts/
└── .gitignore
```

## Critério de apresentação

- Todos os ambientes usam dados fictícios.
- Nenhum segredo, webhook ou credencial real faz parte do repositório.
- Os screenshots foram preparados para leitura rápida, não para documentação exaustiva.
- O foco aqui é mostrar capacidade de entrega, clareza de produto e maturidade de implementação.
