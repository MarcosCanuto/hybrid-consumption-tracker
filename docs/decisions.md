Decisões de Arquitetura
Este documento registra as principais decisões técnicas e de produto tomadas durante o desenvolvimento do MédiaReal, incluindo o raciocínio por trás de cada escolha.

1. Associação correta do consumo ao abastecimento anterior
Decisão: O consumo calculado no momento de um abastecimento é associado ao abastecimento anterior, não ao atual.
Motivação: No momento em que o usuário abastece, ele está encerrando o ciclo do combustível colocado anteriormente. O combustível recém-adicionado ainda não foi consumido. Associar o consumo ao abastecimento atual, como fazem a maioria dos apps, é um erro conceitual que distorce os dados.

2. Sistema de níveis de confiança no cálculo
Decisão: Cada registro de consumo possui um nível de confiança associado, que reflete a precisão do cálculo com base nas informações disponíveis.
Motivação: Em veículos híbridos, raramente é possível saber com exatidão quanto de cada combustível foi utilizado entre dois abastecimentos. Em vez de apresentar um número impreciso como se fosse exato, o sistema é transparente sobre o grau de certeza do cálculo.
Os níveis são:

Alta precisão: ambos os tanques estavam cheios no abastecimento anterior e apenas um tipo de combustível foi detectado no intervalo. O cálculo é exato.
Precisão média: o usuário forneceu informações adicionais como percentual da bateria, percentual do tanque ou odômetro parcial no momento do abastecimento.
Precisão estimada: apenas dados básicos disponíveis. O sistema utiliza médias históricas de consumo do veículo para estimar a distribuição entre os combustíveis.


3. Informações adicionais opcionais, nunca obrigatórias
Decisão: O usuário pode fornecer informações extras para melhorar a precisão de um registro.
Motivação: Tornar o registro de abastecimento simples e rápido é essencial para que o usuário mantenha o hábito de usar o app. A complexidade adicional existe para quem quiser, não para todos.

4. Recálculo automático com confirmação ao editar abastecimentos
Decisão: Ao editar um abastecimento já registrado, o sistema exibe um aviso informando que os registros de consumo afetados serão recalculados. Após confirmação do usuário, o recálculo é feito automaticamente.
Motivação: Edições são esperadas para correção de erros de digitação. O recálculo automático garante a consistência dos dados, enquanto o aviso de confirmação evita recálculos acidentais e mantém o usuário informado sobre o impacto da ação.

5. Arquitetura pensada para escalabilidade desde o início
Decisão: O banco de dados e a API são modelados para suportar múltiplos usuários e múltiplos veículos, mesmo que o MVP foque em um único usuário e veículo.
Motivação: Evitar reescrita futura. Com a estrutura correta desde o início, adicionar suporte a múltiplos usuários no futuro é uma evolução natural, não uma refatoração profunda.

6. Veículos híbridos sem plug-in tratados como veículo de um combustível
Decisão: Veículos HEV (híbridos sem plug-in) são tratados como veículos de combustão simples, pois a bateria é carregada exclusivamente pelo motor e frenagem regenerativa, sem abastecimento elétrico externo.
Motivação: Nesses veículos não há um segundo "abastecimento" elétrico registrável, tornando o cálculo equivalente ao de qualquer veículo convencional.

7. Stack tecnológica
Decisão: React no front-end, FastAPI + Python no back-end, PostgreSQL como banco de dados.
Motivação: As tecnologias foram escolhidas considerando o conhecimento prévio do desenvolvedor (React, Python, SQL), a popularidade no mercado de trabalho brasileiro, e a disponibilidade de planos gratuitos para deploy (Vercel, Railway).