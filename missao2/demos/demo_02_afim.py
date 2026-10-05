import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from missao1.securedocs_math.inverso_multiplicativo import inverso_passos
from securedocs_classica import afim
from securedocs_classica.alfabeto import ALFABETO, normalizar
from textos import MENSAGEM


def mostrar(texto, a, b):
    print("C = (a*P + b) mod 26   e   P = a^-1 * (C - b) mod 26\n")

    print("alfabeto com a = %d, b = %d:" % (a, b))
    print("  claro: %s" % ALFABETO)
    print("  cifra: %s" % afim.cifrar(ALFABETO, a, b))

    cifrado = afim.cifrar(texto, a, b)
    print("\ntexto claro: %s" % normalizar(texto))
    print("chave (a, b) = (%d, %d)" % (a, b))
    print("cifrado    : %s" % cifrado)

    print("\npara decifrar precisa do inverso de a - biblioteca da missão 1:")
    for linha in inverso_passos(a, 26):
        print("  " + linha)
    print("decifrado  : %s" % afim.decifrar(cifrado, a, b))


def main():
    print("=== 2. CIFRA AFIM ===\n")
    mostrar(MENSAGEM, 5, 8)

    print("\nnem todo 'a' serve: com a = 13, A, C, E... viram todas A (e B, D, F... viram N)")
    print("  mdc(13, 26) = 13 -> chave_valida(13) = %s" % afim.chave_valida(13))
    validos = sorted(set(a for a, _ in afim.chaves_validas()))
    print("  valores de a que funcionam: %s" % validos)
    print("  total de chaves: %d x 26 = %d" % (len(validos), len(afim.chaves_validas())))


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    while True:
        a = ler_int("a (coprimo com 26): ", 1, 25)
        if afim.chave_valida(a):
            break
        print("  %d não é coprimo com 26, escolha outro (1, 3, 5, 7, 9, 11, 15...)" % a)
    b = ler_int("b (0 a 25): ", 0, 25)
    print()
    mostrar(texto, a, b)


if __name__ == "__main__":
    main()
