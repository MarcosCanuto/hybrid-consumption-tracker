CREATE TABLE usuarios (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    unidade_consumo_eletrico VARCHAR(20) NOT NULL DEFAULT 'km_kwh',
    unidade_consumo_combustivel VARCHAR(20) NOT NULL DEFAULT 'km_l',
    data_criacao TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE veiculos (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_usuario UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    apelido VARCHAR(100) NOT NULL,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    ano INTEGER,
    data_criacao TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE tanques (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_veiculo BIGINT NOT NULL REFERENCES veiculos(id) on DELETE CASCADE,
    tipo VARCHAR(20) NOT NULL,
    unidade VARCHAR(20) NOT NULL,
    capacidade DECIMAL(8,2)
);

CREATE TABLE tanques_combustivel (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_tanque BIGINT NOT NULL REFERENCES tanques(id) ON DELETE CASCADE,
    tipo_combustivel VARCHAR(50) NOT NULL
);

CREATE TABLE registros (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_veiculo BIGINT NOT NULL REFERENCES veiculos(id) ON DELETE CASCADE,
    id_tanque BIGINT REFERENCES tanques(id) ON DELETE CASCADE,
    id_combustivel BIGINT REFERENCES tanques_combustivel(id) ON DELETE CASCADE,
    tipo VARCHAR(20) NOT NULL,
    data TIMESTAMPTZ NOT NULL,
    odometro DECIMAL(10,2) NOT NULL,
    quantidade DECIMAL(8,3),
    valor_total DECIMAL(10,2),
    valor_unitario DECIMAL(10,4),
    tanque_cheio BOOLEAN DEFAULT FALSE,
    percentual_tanque DECIMAL(5,2),
    percentual_bateria DECIMAL(5,2),
    observacao TEXT,
    data_criacao TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE consumos (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_registro_origem INTEGER NOT NULL REFERENCES registros(id) ON DELETE CASCADE,
    id_registro_destino INTEGER NOT NULL REFERENCES registros(id) ON DELETE CASCADE,
    tipo VARCHAR(20) NOT NULL,
    km_percorridos DECIMAL(10,2) NOT NULL,
    km_percorridos_eletrico DECIMAL(10,2),
    km_percorridos_combustao DECIMAL(10,2),
    consumo_eletrico DECIMAL(8,4),
    consumo_combustao DECIMAL(8,4),
    nivel_confianca DECIMAL(5,2) NOT NULL,
    data_calculo TIMESTAMPTZ NOT NULL DEFAULT NOW()
);