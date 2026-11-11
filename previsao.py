"""Regressão linear simples pelo método dos mínimos quadrados."""


def ajustar_reta(x, y):
    """Devolve (intercepto, inclinacao) da reta y = a + b*x."""
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("O histórico precisa ter ao menos dois pares de dados.")
    media_x = sum(x) / len(x)
    media_y = sum(y) / len(y)
    denominador = sum((valor - media_x) ** 2 for valor in x)
    if denominador == 0:
        raise ValueError("As velocidades do vento não podem ser todas iguais.")
    inclinacao = sum((xi - media_x) * (yi - media_y)
                     for xi, yi in zip(x, y)) / denominador
    intercepto = media_y - inclinacao * media_x
    return intercepto, inclinacao


def prever_energia_eolica(vento_ms, historico):
    if vento_ms < 0:
        raise ValueError("A velocidade do vento não pode ser negativa.")
    a, b = ajustar_reta(historico["vento_ms"], historico["energia_eolica_kwh"])
    # O exemplo é didático: não modela limites físicos da turbina.
    return max(0.0, a + b * vento_ms)
