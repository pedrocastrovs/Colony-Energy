"""Análise das fontes, do consumo e do armazenamento de energia."""

from previsao import prever_energia_eolica


def analisar_energia(colonia):
    sistema = colonia["sistema_energetico"]
    fontes = sistema["fontes"]
    consumo = sistema["consumo"]
    bateria = sistema["bateria"]
    solar = fontes["solar"]["geracao_kwh"]
    eolica = prever_energia_eolica(fontes["eolica"]["vento_ms"], colonia["historico"])
    essencial = sum(consumo["essencial"].values())
    nao_essencial = sum(consumo["nao_essencial"].values())
    return {
        "solar_kwh": solar,
        "eolica_kwh": eolica,
        "geracao_kwh": solar + eolica,
        "essencial_kwh": essencial,
        "nao_essencial_kwh": nao_essencial,
        "consumo_original_kwh": essencial + nao_essencial,
        "bateria_inicial_kwh": bateria["atual_kwh"],
        "capacidade_kwh": bateria["capacidade_kwh"],
        "reserva_minima_kwh": bateria["reserva_minima_kwh"],
    }


def calcular_armazenamento(geracao_kwh, consumo_kwh, bateria_kwh, capacidade_kwh):
    """Saldo para 1 hora; sem perdas de conversão nem limites de potência."""
    saldo = geracao_kwh - consumo_kwh
    if saldo >= 0:
        armazenado = min(saldo, capacidade_kwh - bateria_kwh)
        return {
            "bateria_final_kwh": bateria_kwh + armazenado,
            "armazenado_kwh": armazenado,
            "retirado_kwh": 0.0,
            "excedente_nao_armazenado_kwh": saldo - armazenado,
            "demanda_nao_atendida_kwh": 0.0,
        }
    retirado = min(-saldo, bateria_kwh)
    return {
        "bateria_final_kwh": bateria_kwh - retirado,
        "armazenado_kwh": 0.0,
        "retirado_kwh": retirado,
        "excedente_nao_armazenado_kwh": 0.0,
        "demanda_nao_atendida_kwh": -saldo - retirado,
    }
