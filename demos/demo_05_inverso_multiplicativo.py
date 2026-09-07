import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entrada import ler_int
from securedocs_math.inverso_multiplicativo import (inverso_multiplicativo, tem_inverso,
                                                    inverso_forca_bruta, inverso_passos)


def main():
    print("=== 5. INVERSO MULTIPLICATIVO ===\n")

    for linha in inverso_passos(3, 11):
        print(linha)

    print("\ncom números maiores:")
    for linha in inverso_passos(17, 3120):
        print(linha)

    print("\nsó existe se mdc(a, n) = 1:")
    for linha in inverso_passos(6, 9):
        print(linha)
    print("tem_inverso(6, 9) =", tem_inverso(6, 9))
    try:
        inverso_multiplicativo(6, 9)
    except ValueError as erro:
        print("inverso_multiplicativo(6, 9) -> ValueError:", erro)

    print("\nquem tem inverso em Z_12:")
    for a in range(1, 12):
        inv = inverso_forca_bruta(a, 12)
        if inv is None:
            print("  %2d: não tem" % a)
        else:
            print("  %2d: inverso = %d" % (a, inv))


def interativo():
    n = ler_int("módulo n = ", 2)
    a = ler_int("a = ", 1)

    print()
    for linha in inverso_passos(a, n):
        print(linha)

    if tem_inverso(a, n) and n <= 100000:
        print("\n  conferindo por força bruta: %s" % inverso_forca_bruta(a, n))


if __name__ == "__main__":
    main()
