# MédiaReal
Aplicação web para registro de abastecimentos e cálculo otimizado de consumo de veículos híbridos plug-in (PHEV), com suporte a veículos movidos a um único combustível.

## O problema

A maioria dos aplicativos de controle de abastecimento comete dois erros fundamentais:

1. **Associam o consumo calculado ao combustível recém-abastecido**, quando na verdade o consumo medido no momento do abastecimento pertence ao combustível anterior.
2. **Não consideram que, entre dois abastecimentos, podem ter sido utilizados dois tipos de combustível** (elétrico e gasolina). Isso torna o cálculo impreciso ou simplesmente errado para veículos híbridos.

## A solução

O MédiaReal calcula o consumo associando-o corretamente ao abastecimento anterior e estima, com base no histórico do veículo, a distribuição do consumo entre combustível elétrico e combustão. Cada registro exibe um **nível de confiança** do cálculo, que varia conforme as informações disponíveis:

- **Alta precisão:** ambos os tanques estavam cheios no abastecimento anterior e apenas um tipo de combustível foi utilizado no intervalo.
- **Precisão média:** o usuário forneceu informações adicionais no momento do abastecimento, como percentual da bateria, percentual do tanque ou odômetro parcial.
- **Precisão estimada:** apenas os dados básicos de abastecimento e hodômetro estão disponíveis. O sistema utiliza o histórico para estimar a distribuição entre os combustíveis.

O usuário pode optar por fornecer informações adicionais para melhorar a precisão de um registro, mas isso nunca é obrigatório.

## Funcionalidades

- Registro de abastecimentos com data, hodômetro e quantidade abastecida
- Suporte a múltiplos tipos de combustível por veículo (elétrico, gasolina, etc.)
- Cálculo automático de consumo com nível de confiança da média calculada
- Estimativa de distribuição de consumo entre combustíveis para veículos híbridos
- Histórico de abastecimentos e evolução do consumo
- Gráficos de consumo ao longo do tempo
- Suporte a múltiplos veículos e usuários

## Tecnologias

As tecnologias a serem aplicadas poderão sofrer mudanças durante o desenvolvimento do projeto, uma vez que o mesmo está em fase de arquitetura, tendo sido estabelecidas as seguintes até o momento:

| Camada | Tecnologia |
|--------|-----------|
| Front-end | React, Tailwind CSS |
| Back-end | Python com FastAPI |
| Banco de dados | PostgreSQL |
| Testes | a definir |
| Deploy | a definir |

## Status do projeto

🚧 Em desenvolvimento — fase de planejamento e modelagem

- [x] Definição do problema e solução
- [x] Decisões de arquitetura
- [ ] Modelagem do banco de dados
- [ ] Back-end — endpoints básicos
- [ ] Lógica de cálculo de consumo e nível de confiança
- [ ] Front-end
- [ ] Testes
- [ ] Deploy

## Como executar localmente

> Instruções serão adicionadas conforme o projeto avançar.

## Documentação

- [Decisões de arquitetura](docs/decisions.md)
- [Modelo do banco de dados](docs/database-model.md)