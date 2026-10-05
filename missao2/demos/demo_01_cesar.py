import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from securedocs_classica import cesar
from securedocs_classica.alfabeto import ALFABETO
from textos import MENSAGEM


def main():
    print("=== 1. CIFRA DE CÉSAR ===\n")
    print("C = (P + k) mod 26   e   P = (C - k) mod 26\n")

    print("alfabeto deslocado de 3:")
    print("  claro: %s" % ALFABETO)
    print("  cifra: %s" % cesar.cifrar(ALFABETO, 3))

    cifrado = cesar.cifrar(MENSAGEM, 3)
    print("\ntexto claro: %s" % MENSAGEM)
    print("chave k = 3 (a do próprio César)")
    print("cifrado    : %s" % cifrado)
    print("decifrado  : %s" % cesar.decifrar(cifrado, 3))


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    k = ler_int("chave (1 a 25): ", 1, 25)
    cifrado = cesar.cifrar(texto, k)
    print("\ncifrado  : %s" % cifrado)
    print("decifrado: %s" % cesar.decifrar(cifrado, k))


if __name__ == "__main__":
    main()
