import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entrada import ler_int
from securedocs_math.aritmetica_modular import (mod, soma_mod, sub_mod, mult_mod,
                                                congruentes, tabela_mod, ordem_multiplicativa)


def main():
    print("=== 1. ARITMÉTICA MODULAR ===\n")

    print("resto sempre positivo:")
    print("  mod(-7, 3) =", mod(-7, 3), "(em C daria -1)")
    print("  mod(17, 12) =", mod(17, 12), "(17h = 5 da tarde)")

    print("\ncongruência:")
    print("  17 = 5 (mod 12)?", congruentes(17, 5, 12))
    print("  17 = 6 (mod 12)?", congruentes(17, 6, 12))

    print("\nreduzir no meio da conta dá o mesmo resultado:")
    a, b, n = 123456, 654321, 97
    print("  (a*b) mod n =", (a * b) % n)
    print("  ((a mod n)*(b mod n)) mod n =", mult_mod(mod(a, n), mod(b, n), n))
    print("  -> nunca precisa guardar número maior que n^2")

    print("\ntabela de Z_5 para *:")
    for i, linha in enumerate(tabela_mod(5, "*")):
        print("  ", i, "|", " ".join(str(v) for v in linha))

    print("\nordem multiplicativa em Z_7:")
    for a in (2, 3, 6):
        print("  ordem de", a, "=", ordem_multiplicativa(a, 7))
    print("  9 + 5 mod 12 =", soma_mod(9, 5, 12))


def interativo():
    n = ler_int("módulo n = ", 1)
    a = ler_int("a = ")
    b = ler_int("b = ")

    print()
    print("  %d mod %d = %d" % (a, n, mod(a, n)))
    print("  %d mod %d = %d" % (b, n, mod(b, n)))
    print("  (%d + %d) mod %d = %d" % (a, b, n, soma_mod(a, b, n)))
    print("  (%d - %d) mod %d = %d" % (a, b, n, sub_mod(a, b, n)))
    print("  (%d * %d) mod %d = %d" % (a, b, n, mult_mod(a, b, n)))
    print("  %d e %d são congruentes mod %d? %s" % (a, b, n, congruentes(a, b, n)))

    if 1 < n <= 12:
        print("\n  tabela de Z_%d para *:" % n)
        for i, linha in enumerate(tabela_mod(n, "*")):
            print("   ", i, "|", " ".join(str(v) for v in linha))

    if n <= 100000:
        try:
            print("\n  ordem de %d em Z_%d = %d" % (a, n, ordem_multiplicativa(a, n)))
        except ValueError:
            print("\n  %d não é coprimo com %d, então não tem ordem multiplicativa" % (a, n))
    else:
        print("\n  (módulo grande: pulando a ordem multiplicativa)")


if __name__ == "__main__":
    main()
