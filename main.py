import os
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PASTA, "demos"))

import demo_01_aritmetica_modular
import demo_02_mdc
import demo_03_euclides
import demo_04_euclides_estendido
import demo_05_inverso_multiplicativo
import demo_06_primos
import demo_07_phi_euler
import demo_08_exponenciacao_modular
import demo_09_tcr

import demo_securedocs

ALGORITMOS = [
    ("Aritmética modular", demo_01_aritmetica_modular),
    ("MDC", demo_02_mdc),
    ("Algoritmo de Euclides", demo_03_euclides),
    ("Euclides estendido", demo_04_euclides_estendido),
    ("Inverso multiplicativo", demo_05_inverso_multiplicativo),
    ("Números primos", demo_06_primos),
    ("Função phi de Euler", demo_07_phi_euler),
    ("Exponenciação modular", demo_08_exponenciacao_modular),
    ("Teorema Chinês do Resto", demo_09_tcr),
]


def mostrar_menu():
    print()
    print("=" * 58)
    print(" SecureDocs - Missão 1: algoritmos de teoria dos números")
    print("=" * 58)
    for i, (nome, _) in enumerate(ALGORITMOS, 1):
        print("  %d - %s" % (i, nome))
    print(" 10 - Prova de conceito: RSA (cifrar, assinar, atacar)")
    print(" 11 - Rodar todas as demonstrações seguidas")
    print("  0 - Sair")


def escolher_modo(nome, modulo):
    print("\n%s" % nome)
    print("  1 - ver o exemplo pronto")
    print("  2 - digitar meus próprios valores")
    opcao = input("  opção: ").strip()
    print()
    if opcao == "1":
        modulo.main()
    elif opcao == "2":
        modulo.interativo()
    else:
        print("opção inválida")


def rodar_todas():
    for nome, modulo in ALGORITMOS:
        modulo.main()
        print()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # acentos no terminal do Windows

    while True:
        mostrar_menu()
        escolha = input("\nescolha: ").strip()

        if escolha == "0":
            break
        elif escolha == "10":
            escolher_modo("RSA", demo_securedocs)
        elif escolha == "11":
            print()
            rodar_todas()
        elif escolha.isdigit() and 1 <= int(escolha) <= 9:
            nome, modulo = ALGORITMOS[int(escolha) - 1]
            escolher_modo(nome, modulo)
        else:
            print("opção inválida")
            continue

        input("\n[enter para voltar ao menu] ")


if __name__ == "__main__":
    main()
