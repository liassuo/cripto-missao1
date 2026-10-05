import os
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PASTA, "demos"))

import demo_01_cesar
import demo_02_afim
import demo_03_substituicao
import demo_04_vigenere
import demo_05_hill
import demo_06_transposicao
import demo_07_fluxo
import demo_08_mensagem_interceptada
import demo_09_forca_bruta
import demo_10_frequencia
import demo_11_outros_ataques
import demo_12_kerckhoffs

TECNICAS = [
    ("Cifra de César", demo_01_cesar),
    ("Cifra afim", demo_02_afim),
    ("Substituição monoalfabética", demo_03_substituicao),
    ("Cifra de Vigenère", demo_04_vigenere),
    ("Cifra de Hill", demo_05_hill),
    ("Transposição (colunar e cerca de trilhos)", demo_06_transposicao),
    ("Cifras de fluxo (Vernam e gerador)", demo_07_fluxo),
    ("A mensagem interceptada com cada técnica", demo_08_mensagem_interceptada),
]

ATAQUES = [
    ("Força bruta", demo_09_forca_bruta),
    ("Análise de frequência", demo_10_frequencia),
    ("Outros ataques (Vigenère, Hill, fluxo)", demo_11_outros_ataques),
    ("Princípio de Kerckhoffs", demo_12_kerckhoffs),
]

ALGORITMOS = TECNICAS + ATAQUES
TODAS = len(ALGORITMOS) + 1


def mostrar_menu():
    print()
    print("=" * 58)
    print(" SecureDocs - Missão 2: a mensagem interceptada")
    print("=" * 58)
    print(" A SOLUÇÃO: técnicas para cifrar a mensagem")
    for i, (nome, _) in enumerate(TECNICAS, 1):
        print(" %2d - %s" % (i, nome))
    print("\n O PROBLEMA ADICIONAL: quebrando as cifras")
    for i, (nome, _) in enumerate(ATAQUES, len(TECNICAS) + 1):
        print(" %2d - %s" % (i, nome))
    print()
    print(" %2d - Rodar todas as demonstrações seguidas" % TODAS)
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
    for _, modulo in ALGORITMOS:
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
        elif escolha == str(TODAS):
            print()
            rodar_todas()
        elif escolha.isdigit() and 1 <= int(escolha) <= len(ALGORITMOS):
            nome, modulo = ALGORITMOS[int(escolha) - 1]
            escolher_modo(nome, modulo)
        else:
            print("opção inválida")
            continue

        input("\n[enter para voltar ao menu] ")


if __name__ == "__main__":
    main()
