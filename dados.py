"""Estruturas de dados da colônia: listas e dicionários hierárquicos."""

HISTORICO = {
    "vento_ms": [8.0, 10.0, 12.0, 14.0],
    "energia_eolica_kwh": [20.0, 25.0, 30.0, 35.0],
}


def criar_colonia(solar_kwh=15.0, vento_ms=11.0, essencial_kwh=50.0,
                  nao_essencial_kwh=20.0, bateria_kwh=40.0,
                  capacidade_kwh=100.0, reserva_minima_kwh=20.0):
    """Cria uma estrutura hierárquica para simular um intervalo de uma hora."""
    valores = [solar_kwh, vento_ms, essencial_kwh, nao_essencial_kwh,
               bateria_kwh, capacidade_kwh, reserva_minima_kwh]
    if any(v < 0 for v in valores):
        raise ValueError("Os valores não podem ser negativos.")
    if bateria_kwh > capacidade_kwh:
        raise ValueError("A bateria atual não pode ultrapassar a capacidade.")
    if reserva_minima_kwh > capacidade_kwh:
        raise ValueError("A reserva mínima não pode ultrapassar a capacidade.")
    return {
        "sistema_energetico": {
            "fontes": {
                "solar": {"geracao_kwh": float(solar_kwh)},
                "eolica": {"vento_ms": float(vento_ms)},
            },
            "consumo": {
                "essencial": {"suporte_a_vida_e_servicos_basicos_kwh": float(essencial_kwh)},
                "nao_essencial": {"cargas_desligaveis_kwh": float(nao_essencial_kwh)},
            },
            "bateria": {
                "atual_kwh": float(bateria_kwh),
                "capacidade_kwh": float(capacidade_kwh),
                "reserva_minima_kwh": float(reserva_minima_kwh),
            },
        },
        "historico": {
            "vento_ms": HISTORICO["vento_ms"].copy(),
            "energia_eolica_kwh": HISTORICO["energia_eolica_kwh"].copy(),
        },
    }


CENARIOS = {
    "normal": dict(solar_kwh=55, vento_ms=10, essencial_kwh=50,
                   nao_essencial_kwh=20, bateria_kwh=35),
    "economia": dict(solar_kwh=30, vento_ms=10, essencial_kwh=50,
                     nao_essencial_kwh=20, bateria_kwh=55),
    "critico": dict(solar_kwh=15, vento_ms=11, essencial_kwh=50,
                    nao_essencial_kwh=20, bateria_kwh=40),
    "excedente": dict(solar_kwh=80, vento_ms=12, essencial_kwh=40,
                      nao_essencial_kwh=10, bateria_kwh=95),
    "insuficiencia": dict(solar_kwh=5, vento_ms=8, essencial_kwh=50,
                         nao_essencial_kwh=20, bateria_kwh=5),
}
