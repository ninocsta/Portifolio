# Features

## Listagem com filtro reativo
- Componente de listagem que consome API REST Countries
- Filtro por nome em tempo real com `debounceTime` e `distinctUntilChanged`
- Exibição de bandeira, nome, capital e população
- Pipe personalizado para formatação de números populacionais

## Detalhe de item
- Rota `/country/:code` com carregamento sob demanda
- Exibe dados completos: idiomas, moedas, países vizinhos
- Botão de voltar com navegação programática

## Formulário com validação reativa
- Formulário de "favoritos" com validação em tempo real
- Campos com mensagens de erro contextuais
- Submit desabilitado enquanto inválido

## Organização de código
- Feature modules com lazy loading
- Serviço isolado (`CountryService`) com métodos tipados
- Interfaces TypeScript para os modelos de dados (Country, Currency, Language)
