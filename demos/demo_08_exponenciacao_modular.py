import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entrada import ler_int
from securedocs_math.exponenciacao_modular import exp_mod, exp_mod_ingenua, exp_mod_passos


def main():
    print("=== 8. EXPONENCIAÇÃO MODULAR ===\n")

    print("7^13 mod 11 passo a passo (13 = 1101 em binário):")
    for linha in exp_mod_passos(7, 13, 11):
        print("  " + linha)

    print("\nexemplo do RSA do livro: 4^13 mod 497 =", exp_mod(4, 13, 497))

    print("\ningênua O(e) x rápida O(log e):")
    base, n = 7, 1000003
    for e in (10**5, 10**6, 10**7):
        inicio = time.time()
        r1 = exp_mod_ingenua(base, e, n)
        t1 = time.time() - inicio
        inicio = time.time()
        r2 = exp_mod(base, e, n)
        t2 = time.time() - inicio
        assert r1 == r2
        print("  e = %-8d ingênua %.3f s | rápida %.6f s" % (e, t1, t2))

    print("\nexpoente de 65537 no RSA:")
    print("  7^65537 inteiro teria uns", int(65537 * 0.845), "dígitos")
    print("  exp_mod(7, 65537, 1000003) =", exp_mod(7, 65537, 1000003), "(na hora)")

    print("\nexpoente negativo = inverso: 3^-1 mod 11 =", exp_mod(3, -1, 11))


def interativo():
    base = ler_int("base = ")
    expoente = ler_int("expoente = ")
    n = ler_int("módulo n = ", 1)

    print()
    if 0 <= expoente <= 4096:
        for linha in exp_mod_passos(base, expoente, n):
            print("  " + linha)
    else:
        print("  %d^%d mod %d = %d" % (base, expoente, n, exp_mod(base, expoente, n)))

    if 0 <= expoente <= 10**6:
        inicio = time.time()
        exp_mod(base, expoente, n)
        t1 = time.time() - inicio
        inicio = time.time()
        exp_mod_ingenua(base, expoente, n)
        t2 = time.time() - inicio
        print("\n  rápida: %.6f s | ingênua: %.6f s" % (t1, t2))


if __name__ == "__main__":
    main()
