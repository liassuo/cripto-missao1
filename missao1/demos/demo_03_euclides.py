import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int
from securedocs_math.euclides import euclides, euclides_recursivo, euclides_passos


def main():
    print("=== 3. ALGORITMO DE EUCLIDES ===\n")

    print("passo a passo:")
    for linha in euclides_passos(1071, 462):
        print("  " + linha)

    print("\niterativo x recursivo:")
    print("  euclides(1071, 462) =", euclides(1071, 462))
    print("  euclides_recursivo(1071, 462) =", euclides_recursivo(1071, 462))

    print("\nquantidade de divisões cresce devagar:")
    pares = [(48, 18), (1071, 462), (2**64 - 1, 2**32 - 1), (10**30 + 7, 10**15 + 3)]
    for a, b in pares:
        n = len(euclides_passos(a, b)) - 2
        print("  menor número com %2d dígitos -> %2d divisões" % (len(str(min(a, b))), n))

    print("\npior caso (Fibonacci seguidos):")
    for linha in euclides_passos(89, 55):
        print("  " + linha)


def interativo():
    a = ler_int("a = ", 1)
    b = ler_int("b = ", 1)

    print()
    for linha in euclides_passos(a, b):
        print("  " + linha)
    print("\n  foram %d divisões" % (len(euclides_passos(a, b)) - 2))


if __name__ == "__main__":
    main()
