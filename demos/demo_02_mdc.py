import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entrada import ler_int
from securedocs_math.mdc import divisores, mdc_ingenuo, mdc, mmc, coprimos


def main():
    print("=== 2. MDC ===\n")

    print("pela definição (divisores em comum):")
    print("  divisores(1071) =", divisores(1071))
    print("  divisores(462)  =", divisores(462))
    print("  maior em comum -> mdc_ingenuo(1071, 462) =", mdc_ingenuo(1071, 462))

    print("\nversão rápida (Euclides):")
    print("  mdc(1071, 462) =", mdc(1071, 462))

    print("\ncomparando o tempo com dois números de 13 dígitos:")
    a = 10**12 + 39
    b = 10**12 + 61
    inicio = time.time()
    g1 = mdc_ingenuo(a, b)
    t1 = time.time() - inicio
    inicio = time.time()
    g2 = mdc(a, b)
    t2 = time.time() - inicio
    print("  ingênuo :", g1, "em %.3f s" % t1)
    print("  Euclides:", g2, "em %.6f s" % t2)

    print("\nmmc e coprimos:")
    print("  mmc(4, 6) =", mmc(4, 6))
    print("  coprimos(8, 9) =", coprimos(8, 9), "| coprimos(8, 12) =", coprimos(8, 12))
    print("  e=65537 é coprimo com phi=3120?", coprimos(65537, 3120), "(condição do RSA)")


def interativo():
    a = ler_int("a = ", 1)
    b = ler_int("b = ", 1)

    print()
    if a <= 10**9 and b <= 10**9:
        print("  divisores de %d: %s" % (a, divisores(a)))
        print("  divisores de %d: %s" % (b, divisores(b)))
        print("  mdc pela definição = %d" % mdc_ingenuo(a, b))
    else:
        print("  (números grandes: pulando a listagem de divisores)")
    print("  mdc por Euclides   = %d" % mdc(a, b))
    print("  mmc = %d" % mmc(a, b))
    print("  são coprimos? %s" % coprimos(a, b))


if __name__ == "__main__":
    main()
