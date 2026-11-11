"""Colony Energy - sistema integrado de gestão energética da colônia."""

import argparse
from dados import CENARIOS, criar_colonia, HISTORICO
from decisoes import avaliar_colonia
from previsao import ajustar_reta


def mostrar(resultado, titulo="Resultado da simulação"):
    print("\n" + "=" * 58)
    print(titulo.upper())
    print("=" * 58)
    print(f"Modo de operação        : {resultado['modo']}")
    print(f"Geração solar           : {resultado['solar_kwh']:.1f} kWh")
    print(f"Geração eólica prevista : {resultado['eolica_kwh']:.1f} kWh")
    print(f"Geração total           : {resultado['geracao_kwh']:.1f} kWh")
    print(f"Consumo original        : {resultado['consumo_original_kwh']:.1f} kWh")
    print(f"Consumo após decisão    : {resultado['consumo_ajustado_kwh']:.1f} kWh")
    print(f"Economia de energia     : {resultado['economia_kwh']:.1f} kWh")
    print(f"Bateria inicial / final : {resultado['bateria_inicial_kwh']:.1f} / "
          f"{resultado['bateria_final_kwh']:.1f} kWh")
    print(f"Energia armazenada      : {resultado['armazenado_kwh']:.1f} kWh")
    print(f"Energia da bateria usada: {resultado['retirado_kwh']:.1f} kWh")
    print(f"Excedente não armazenado: {resultado['excedente_nao_armazenado_kwh']:.1f} kWh")
    print(f"Demanda não atendida    : {resultado['demanda_nao_atendida_kwh']:.1f} kWh")
    print(f"DECISÃO                 : {resultado['acao']}")
    for alerta in resultado["alertas"]:
        print(f"ALERTA                  : {alerta}")


def simular_cenario(nome):
    resultado = avaliar_colonia(criar_colonia(**CENARIOS[nome]))
    mostrar(resultado, f"Cenário: {nome}")
    return resultado


def obter_float(rotulo, padrao):
    while True:
        texto = input(f"{rotulo} [{padrao}]: ").strip().replace(",", ".")
        try:
            valor = float(texto) if texto else float(padrao)
            if valor < 0:
                raise ValueError
            return valor
        except ValueError:
            print("Informe um número maior ou igual a zero.")


def entrada_personalizada():
    print("\nInforme os dados para 1 hora (Enter aceita o padrão):")
    campos = {
        "solar_kwh": obter_float("Geração solar (kWh)", 15),
        "vento_ms": obter_float("Velocidade do vento (m/s)", 11),
        "essencial_kwh": obter_float("Consumo essencial (kWh)", 50),
        "nao_essencial_kwh": obter_float("Consumo não essencial (kWh)", 20),
        "bateria_kwh": obter_float("Bateria atual (kWh)", 40),
        "capacidade_kwh": obter_float("Capacidade da bateria (kWh)", 100),
        "reserva_minima_kwh": obter_float("Reserva mínima (kWh)", 20),
    }
    try:
        mostrar(avaliar_colonia(criar_colonia(**campos)), "Cenário personalizado")
    except ValueError as exc:
        print(f"Dados inválidos: {exc}")


def exibir_modelo():
    a, b = ajustar_reta(HISTORICO["vento_ms"], HISTORICO["energia_eolica_kwh"])
    print("\nDADOS HISTÓRICOS (didáticos, intervalos de 1 hora)")
    for x, y in zip(HISTORICO["vento_ms"], HISTORICO["energia_eolica_kwh"]):
        print(f"  Vento: {x:.1f} m/s -> Energia eólica: {y:.1f} kWh")
    print(f"Modelo ajustado: energia = {a:.2f} + {b:.2f} × vento")
    print(f"Previsão para 11 m/s: {a + b * 11:.1f} kWh")


def menu():
    while True:
        print("\nCOLONY ENERGY | 1-Simulação crítica | 2-Inserir dados")
        print("3-Executar 5 cenários | 4-Ver regressão linear | 0-Sair")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            simular_cenario("critico")
        elif opcao == "2":
            entrada_personalizada()
        elif opcao == "3":
            for nome in CENARIOS:
                simular_cenario(nome)
        elif opcao == "4":
            exibir_modelo()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def principal():
    parser = argparse.ArgumentParser(description="Sistema de gestão energética da colônia")
    parser.add_argument("--demo", action="store_true", help="Executa todos os cenários sem interação")
    parser.add_argument("--cenario", choices=list(CENARIOS), help="Executa um cenário de teste")
    args = parser.parse_args()
    if args.demo:
        exibir_modelo()
        for nome in CENARIOS:
            simular_cenario(nome)
    elif args.cenario:
        simular_cenario(args.cenario)
    else:
        menu()


if __name__ == "__main__":
    principal()
