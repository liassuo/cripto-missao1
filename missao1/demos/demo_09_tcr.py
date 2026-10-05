import os
import sys
import time
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int
from securedocs_math.exponenciacao_modular import exp_mod
from securedocs_math.inverso_multiplicativo import inverso_multiplicativo
from securedocs_math.primos import gerar_primo
from securedocs_math.tcr import tcr, tcr_passos, decompor


def main():
    print("=== 9. TEOREMA CHINÊS DO RESTO ===\n")

    modulos = [7, 11, 13]

    print("x = 3 (mod 7), x = 4 (mod 11), x = 5 (mod 13):")
    for linha in tcr_passos([3, 4, 5], modulos):
        print("  " + linha)

    print("\nida e volta (cada módulo é uma 'coordenada'):")
    for x in (54, 713, 1000):
        restos = decompor(x, modulos)
        volta, M = tcr(restos, modulos)
        print("  x = %4d -> restos %s -> tcr -> %d (mod %d)" % (x, restos, volta, M))

    print("\ndá para somar e multiplicar direto nos restos:")
    a, b = 23, 31
    resto_a = decompor(a, modulos)
    resto_b = decompor(b, modulos)
    soma = [(x + y) % m for x, y, m in zip(resto_a, resto_b, modulos)]
    produto = [(x * y) % m for x, y, m in zip(resto_a, resto_b, modulos)]
    print("  a = %d -> %s" % (a, resto_a))
    print("  b = %d -> %s" % (b, resto_b))
    print("  soma nos restos    %s -> tcr -> %d (a + b = %d)" % (soma, tcr(soma, modulos)[0], a + b))
    print("  produto nos restos %s -> tcr -> %d (a * b = %d)" % (produto, tcr(produto, modulos)[0], a * b))
    print("  -> três contas pequenas no lugar de uma grande, e nenhuma passa de 13")

    print("\nmódulos não coprimos:")
    try:
        tcr([1, 2], [4, 6])
    except ValueError as erro:
        print("  tcr([1, 2], [4, 6]) -> ValueError:", erro)

    print("\ncom dois primos grandes: contas mod p e mod q, juntadas pelo TCR")
    p = gerar_primo(512)
    q = gerar_primo(512)
    n = p * q
    e = 65537
    d = inverso_multiplicativo(e, (p - 1) * (q - 1))
    m = 123456789
    c = exp_mod(m, e, n)

    inicio = time.time()
    for _ in range(20):
        direto = exp_mod(c, d, n)
    t_direto = time.time() - inicio

    dp = d % (p - 1)
    dq = d % (q - 1)
    inicio = time.time()
    for _ in range(20):
        via_tcr, _ = tcr([exp_mod(c, dp, p), exp_mod(c, dq, q)], [p, q])
    t_tcr = time.time() - inicio

    print("  direto: %.4f s | com TCR: %.4f s (%.1fx mais rápido)" % (t_direto, t_tcr, t_direto / t_tcr))
    print("  mesmo resultado?", direto == via_tcr == m)


def interativo():
    quantas = ler_int("quantas congruências? ", 2, 6)
    restos = []
    modulos = []
    for i in range(quantas):
        print("  congruência %d:" % (i + 1))
        restos.append(ler_int("    resto  a = "))
        modulos.append(ler_int("    módulo n = ", 1))

    print()
    try:
        for linha in tcr_passos(restos, modulos):
            print("  " + linha)
    except ValueError as erro:
        print("  não deu pra resolver:", erro)
        return

    x, M = tcr(restos, modulos)
    print("\n  conferindo a solução:")
    for a, m in zip(restos, modulos):
        print("    %d mod %d = %d (queria %d)" % (x, m, x % m, a % m))


if __name__ == "__main__":
    main()
