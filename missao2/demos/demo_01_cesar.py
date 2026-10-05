import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from securedocs_classica import cesar
from securedocs_classica.alfabeto import ALFABETO, normalizar
from textos import MENSAGEM


def mostrar(texto, k):
    print("C = (P + k) mod 26   e   P = (C - k) mod 26\n")

    print("alfabeto deslocado de %d:" % k)
    print("  claro: %s" % ALFABETO)
    print("  cifra: %s" % cesar.cifrar(ALFABETO, k))

    cifrado = cesar.cifrar(texto, k)
    print("\ntexto claro: %s" % normalizar(texto))
    print("chave k = %d" % k)
    print("cifrado    : %s" % cifrado)
    print("decifrado  : %s" % cesar.decifrar(cifrado, k))


def main():
    print("=== 1. CIFRA DE CÉSAR ===\n")
    mostrar(MENSAGEM, 3)


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    k = ler_int("chave (1 a 25): ", 1, 25)
    print()
    mostrar(texto, k)


if __name__ == "__main__":
    main()
