from sqlalchemy.orm import Session
from app.models.registro import Registro
from app.models.consumo import Consumo
from decimal import Decimal

def calcular_consumo(db: Session, registro_atual: Registro) -> Consumo | None:
    # 1. Buscar odômetro anterior para o mesmo veículo, seja checkpoint ou abastecimento.
    registro_anterior = (
        db.query(Registro).filter(
            Registro.id_veiculo == registro_atual.id_veiculo,
            Registro.id < registro_atual.id
        ).order_by(Registro.data.desc()).first()
    )

    # Buscar capacidade da bateria e do tanque para calcular o consumo elétrico e de combustão, com base nas porcentagens (checkpoint).
    from app.models.tanque import Tanque
    tanques = db.query(Tanque).filter(Tanque.id_veiculo == registro_atual.id_veiculo).all()
    tanque_eletrico = next((t for t in tanques if t.tipo == "eletrico"), None)
    tanque_liquido = next((t for t in tanques if t.tipo == "liquido"), None)

    # 2. Se não há registro anterior, é o primeiro registro do veículo, não tem como calcular consumo, ou forçar o registro de um checkpoint no cadastro do veículo para ter um ponto de partida.
    if not registro_anterior:
        return None
    
    # 3. Calcular a distância entre o último registro e o atual
    distancia = float(registro_atual.odometro) - float(registro_anterior.odometro)

    # 4. Se a distância for negativa ou zero, pode ser necessário calcular o quanto o motor recarregou a bateria do veículo.
    
    # 5. Verificar se o registro anterior possui informação de % da bateria, % do tanque para calcular o consumo
    variacao_bateria = None
    variacao_tanque = None

    if registro_anterior.percentual_bateria is not None and registro_atual.percentual_bateria is not None:
        variacao_bateria = float(registro_anterior.percentual_bateria) - float(registro_atual.percentual_bateria)
    else:
        variacao_bateria = None

    if registro_anterior.percentual_tanque is not None and registro_atual.percentual_tanque is not None:
        variacao_tanque = float(registro_anterior.percentual_tanque) - float(registro_atual.percentual_tanque)
    else:
        variacao_tanque = None
    
    #DEBUG PARA ENTENDER PORQUE O CONSUMO NÃO ESTÁ SENDO CALCULADO
    print(f"DEBUG — tipo: {registro_atual.tipo}")
    print(f"DEBUG — variacao_bateria: {variacao_bateria}")
    print(f"DEBUG — variacao_tanque: {variacao_tanque}")
    print(f"DEBUG — distancia: {distancia}")
    print(f"DEBUG — tanque_eletrico id: {tanque_eletrico.id if tanque_eletrico else None}")
    print(f"DEBUG — tanque_liquido id: {tanque_liquido.id if tanque_liquido else None}")
    print(f"DEBUG — registro_atual.id_tanque: {registro_atual.id_tanque}")

    # 6. Se os dois registros forem abastecimento com tanque cheio, sem alteração nos percentuais dos dois tanques, é a melhor situação para o consumo, pois o carro foi abastecido e o tanque ficou cheio, então o consumo é a quantidade abastecida dividida pelos km percorridos.
    if registro_atual.tipo == "abastecimento" and (variacao_bateria == 0 or variacao_tanque == 0) and distancia > 0:
        consumo_eletrico = distancia / float(registro_atual.quantidade) if registro_atual.id_tanque == tanque_eletrico.id else None
        consumo_combustao = distancia / float(registro_atual.quantidade) if registro_atual.id_tanque == tanque_liquido.id else None
        consumo = Consumo(
            id_registro_origem=registro_anterior.id,
            id_registro_destino=registro_atual.id,
            tipo="consumo do trecho",
            km_percorridos=distancia,
            consumo_eletrico=consumo_eletrico,
            consumo_combustao=consumo_combustao,
            nivel_confianca=100.0
        )
        db.add(consumo)
        db.commit()
        db.refresh(consumo)
        return consumo
    
    # 7. Se a variação da bateria  for positiva
        # 7.1 Sem deslocamento
        # 7.2 Com deslocamento
            # 7.2.1 Pode ser CARREGAMENTO na tomada - tipo de registro: 'abastecimento'
        

            # 7.1.2 A bateria pode ter regenerado energia com o carro em movimento, nesse caso o consumo será negativo -tipo do registro: 'checkpoint' 

            # 5.1.1.1 Pode ser CARREGAMENTO na tomada - tipo de registro: 'abastecimento'
            # 5.1.1.2 Pode ser o motor a combustão carregando a bateria, nesse caso a variação do tanque será negativa e a variação da bateria positiva. tipo do registro: 'checkpoint'
        
            # 5.1.2.1 O motor a combustão pode ter carregado a bateria durante o deslocamento
                # 5.1.2.2 Se a variação do tanque for negativa - tipo do registro: 'checkpoint'
                # 5.1.2.3 Se a variação do tanque for positiva - tipo do registro: 'abastecimento'

    # 5.2 Se a variação da bateria for negativa
        # 5.2.1 Sem deslocamento
            # 5.2.1.1 Pode ser que o carro ficou ligado, consumindo bateria, mas sem se mover - tipo do registro: 'checkpoint'
        
        # 5.2.2 Com deslocamento
            # 5.2.2.1 O carro consumiu energia da bateria para se mover.
            # 5.2.2.2 O carro consumiu energia da bateria E do tanque para se mover.
