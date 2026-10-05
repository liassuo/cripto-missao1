import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from missao1.securedocs_math.mdc import mdc
from securedocs_classica import hill
from securedocs_classica.alfabeto import agrupar
from textos import MENSAGEM


def mostrar_matriz(m, recuo="  "):
    for linha in m:
        print(recuo + " ".join("%3d" % x for x in linha))


def main():
    print("=== 5. CIFRA DE HILL ===\n")
    print("blocos de n letras viram vetores; C = K * P (mod 26)\n")

    k = [[3, 3], [2, 5]]
    print("matriz chave K:")
    mostrar_matriz(k)
    det = hill.determinante(k) % 26
    print("det(K) = %d, mdc(%d, 26) = %d -> tem inversa" % (det, det, mdc(det, 26)))
    print("K^-1 (mod 26), usando o inverso multiplicativo da missão 1:")
    mostrar_matriz(hill.inversa(k))
    print("conferindo K * K^-1 =", hill.multiplicar(k, hill.inversa(k)))

    cifrado = hill.cifrar(MENSAGEM, k)
    print("\ntexto claro: %s" % MENSAGEM)
    print("cifrado    : %s" % agrupar(cifrado))
    print("decifrado  : %s" % hill.decifrar(cifrado, k))
    print("(38 letras = 19 blocos de 2; se sobrar letra, completa com X)")

    print("\ncom matriz 3x3 a mesma letra depende das vizinhas:")
    k3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
    mostrar_matriz(k3)
    print("cifrado: %s" % agrupar(hill.cifrar(MENSAGEM, k3)))


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    while True:
        print("matriz 2x2 [[a, b], [c, d]]:")
        k = [[ler_int("  a = ", 0, 25), ler_int("  b = ", 0, 25)],
             [ler_int("  c = ", 0, 25), ler_int("  d = ", 0, 25)]]
        if hill.chave_valida(k):
            break
        det = hill.determinante(k) % 26
        print("  det = %d e mdc(%d, 26) = %d: não tem inversa, tente outra" % (det, det, mdc(det, 26)))
    cifrado = hill.cifrar(texto, k)
    print("\nK^-1 =", hill.inversa(k))
    print("cifrado  : %s" % agrupar(cifrado))
    print("decifrado: %s" % hill.decifrar(cifrado, k))


if __name__ == "__main__":
    main()
