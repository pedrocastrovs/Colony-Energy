"""Regras automáticas de prioridade: preservar consumo essencial."""

from energia import analisar_energia, calcular_armazenamento


def avaliar_colonia(colonia):
    dados = analisar_energia(colonia)
    geracao = dados["geracao_kwh"]
    inicial = dados["bateria_inicial_kwh"]
    consumo_original = dados["consumo_original_kwh"]
    previsao_bateria_sem_acao = inicial + geracao - consumo_original

    # Prioridade: manter os sistemas essenciais; cortar apenas cargas opcionais.
    if geracao >= consumo_original:
        modo = "NORMAL"
        consumo_nao_essencial = dados["nao_essencial_kwh"]
        acao = "Manter operação normal e armazenar excedente, se houver espaço."
    elif previsao_bateria_sem_acao < dados["reserva_minima_kwh"]:
        modo = "CRITICO"
        consumo_nao_essencial = 0.0
        acao = "Desligar cargas NÃO essenciais e priorizar suporte à vida."
    else:
        modo = "ECONOMIA"
        consumo_nao_essencial = dados["nao_essencial_kwh"] * 0.5
        acao = "Reduzir pela metade as cargas não essenciais."

    consumo_ajustado = dados["essencial_kwh"] + consumo_nao_essencial
    armazenamento = calcular_armazenamento(
        geracao, consumo_ajustado, inicial, dados["capacidade_kwh"]
    )
    alertas = []
    if geracao < consumo_original:
        alertas.append("Geração menor que o consumo original.")
    if armazenamento["bateria_final_kwh"] < dados["reserva_minima_kwh"]:
        alertas.append("Reserva de bateria abaixo do mínimo recomendado.")
    if armazenamento["demanda_nao_atendida_kwh"] > 1e-9:
        modo = "EMERGENCIA"
        alertas.append("Energia insuficiente até para atender toda a demanda ajustada.")
        acao = "Solicitar fonte auxiliar e medidas emergenciais para proteger suporte à vida."
    if armazenamento["excedente_nao_armazenado_kwh"] > 1e-9:
        alertas.append("Bateria cheia: há geração excedente não armazenada.")

    return {
        **dados,
        **armazenamento,
        "modo": modo,
        "acao": acao,
        "consumo_ajustado_kwh": consumo_ajustado,
        "economia_kwh": consumo_original - consumo_ajustado,
        "saldo_final_kwh": geracao - consumo_ajustado,
        "alertas": alertas,
        "suporte_a_vida_priorizado": True,
    }
