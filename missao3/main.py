import os
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PASTA, "demos"))

import demo_01_des
import demo_02_rc5
import demo_03_aes
import demo_04_modos
import demo_05_experimento_arquivo
import demo_06_documentos_roubados
import demo_07_comparacao
import demo_08_entregar_chave

ALGORITMOS_SIMETRICOS = [
    ("DES", demo_01_des),
    ("RC5", demo_02_rc5),
    ("AES", demo_03_aes),
    ("Modos de operação (ECB, CBC, CTR)", demo_04_modos),
]

EXPERIMENTO = [
    ("Arquivo original -> AES -> cifrado -> AES -> original", demo_05_experimento_arquivo),
    ("Os documentos roubados: clássica x AES", demo_06_documentos_roubados),
    ("Comparação DES x RC5 x AES e a escolha", demo_07_comparacao),
]

DESCOBERTA = [
    ("Como entregar a chave secreta? (Diffie-Hellman e RSA)", demo_08_entregar_chave),
]

ALGORITMOS = ALGORITMOS_SIMETRICOS + EXPERIMENTO + DESCOBERTA


def mostrar_menu():
    print()
    print("=" * 58)
    print(" SecureDocs - Missão 3: milhares de documentos roubados")
    print("=" * 58)
    print(" O DESAFIO: criptografia simétrica")
    i = 1
    for titulo, grupo in ((None, ALGORITMOS_SIMETRICOS), ("O EXPERIMENTO E A ESCOLHA", EXPERIMENTO),
                          ("NOVA DESCOBERTA", DESCOBERTA)):
        if titulo:
            print("\n " + titulo)
        for nome, _ in grupo:
            print(" %2d - %s" % (i, nome))
            i += 1
    print()
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


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # acentos no terminal do Windows

    while True:
        mostrar_menu()
        escolha = input("\nescolha: ").strip()

        if escolha == "0":
            break
        elif escolha.isdigit() and 1 <= int(escolha) <= len(ALGORITMOS):
            nome, modulo = ALGORITMOS[int(escolha) - 1]
            escolher_modo(nome, modulo)
        else:
            print("opção inválida")
            continue

        input("\n[enter para voltar ao menu] ")


if __name__ == "__main__":
    main()
