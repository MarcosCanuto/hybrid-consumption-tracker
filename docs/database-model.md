# Modelo do Banco de Dados

> 🚧 Este documento será atualizado conforme a modelagem for finalizada.

## Entidades principais

O sistema é estruturado em torno das seguintes entidades e seus relacionamentos:

```
Usuário → tem vários Veículos
Veículo → tem vários Tanques (um por tipo de combustível)
Tanque  → tem vários Abastecimentos
Abastecimento → gera um Registro de Consumo
```

Cada **Registro de Consumo** é calculado no momento de um novo abastecimento e associado ao abastecimento **anterior**, utilizando um ou mais abastecimentos anteriores como base para o cálculo, dependendo das informações disponíveis.

## Diagrama

> O diagrama será adicionado após a finalização da modelagem.

## Descrição das tabelas

> A descrição detalhada das tabelas e colunas será adicionada após a finalização da modelagem.