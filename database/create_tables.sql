CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    unidade_consumo_eletrico VARCHAR(20) NOT NULL DEFAULT 'km_kwh',
    unidade_consumo_combustivel VARCHAR(20) NOT NULL DEFAULT 'km_l',
    data_criacao TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE veiculo (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuario(id),
    apelido VARCHAR(100) NOT NULL,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    ano INTEGER,
    data_criacao TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE tanque (
    id SERIAL PRIMARY KEY,
    id_veiculo INTEGER NOT NULL REFERENCES veiculo(id),
    tipo VARCHAR(20) NOT NULL,
    unidade VARCHAR(20) NOT NULL,
    capacidade DECIMAL(8,2)
);

CREATE TABLE tanque_combustivel (
    id SERIAL PRIMARY KEY,
    id_tanque INTEGER NOT NULL REFERENCES tanque(id),
    tipo_combustivel VARCHAR(50) NOT NULL
);

CREATE TABLE registro (
    id SERIAL PRIMARY KEY,
    id_veiculo INTEGER NOT NULL REFERENCES veiculo(id),
    id_tanque INTEGER REFERENCES tanque(id),
    id_combustivel INTEGER REFERENCES tanque_combustivel(id),
    tipo VARCHAR(20) NOT NULL,
    data TIMESTAMP NOT NULL,
    odometro DECIMAL(10,2) NOT NULL,
    quantidade DECIMAL(8,3),
    valor_total DECIMAL(10,2),
    valor_unitario DECIMAL(10,4),
    tanque_cheio BOOLEAN,
    percentual_tanque DECIMAL(5,2),
    percentual_bateria DECIMAL(5,2),
    observacao TEXT,
    data_criacao TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE consumo (
    id SERIAL PRIMARY KEY,
    id_registro_origem INTEGER NOT NULL REFERENCES registro(id),
    id_registro_destino INTEGER NOT NULL REFERENCES registro(id),
    tipo VARCHAR(20) NOT NULL,
    km_percorridos DECIMAL(10,2) NOT NULL,
    consumo_eletrico DECIMAL(8,4),
    consumo_combustao DECIMAL(8,4),
    nivel_confianca DECIMAL(5,2) NOT NULL,
    data_calculo TIMESTAMP NOT NULL DEFAULT NOW()
);