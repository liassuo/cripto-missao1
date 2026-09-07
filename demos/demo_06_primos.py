import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entrada import ler_int
from securedocs_math.primos import (crivo_eratostenes, eh_primo, eh_primo_forca_bruta,
                                    miller_rabin, gerar_primo, proximo_primo, fatorar,
                                    pollard_rho)


def main():
    print("=== 6. NÚMEROS PRIMOS ===\n")

    print("crivo de Eratóstenes:")
    print("  primos até 50:", crivo_eratostenes(50))
    print("  quantos primos até 10000:", len(crivo_eratostenes(10000)))

    print("\n561 = 3*11*17 engana o teste de Fermat, mas não o Miller-Rabin:")
    print("  2^560 mod 561 =", pow(2, 560, 561), "(Fermat diria que é primo)")
    print("  miller_rabin(561) =", miller_rabin(561))
    print("  força bruta =", eh_primo_forca_bruta(561))

    print("\ngerando primos grandes:")
    for bits in (128, 512, 1024):
        inicio = time.time()
        p = gerar_primo(bits)
        print("  %4d bits em %.3f s: %s..." % (bits, time.time() - inicio, str(p)[:30]))
    print("  próximo primo depois de 1000:", proximo_primo(1000))

    print("\nfatorar é o lado difícil:")
    print("  fatorar(360) =", fatorar(360))
    for bits in (32, 48, 64):
        p = gerar_primo(bits // 2)
        q = gerar_primo(bits // 2)
        inicio = time.time()
        f = pollard_rho(p * q)
        print("  n de %d bits: Pollard rho achou %d em %.4f s" % (bits, f, time.time() - inicio))
    print("  com 2048 bits nenhum algoritmo conhecido termina")


def interativo():
    n = ler_int("número para testar = ", 0)

    print()
    print("  %d é primo? %s" % (n, eh_primo(n)))
    if 2 <= n <= 10**12:
        print("  fatoração: %s" % fatorar(n))
    print("  próximo primo depois de %d: %d" % (n, proximo_primo(n)))

    bits = ler_int("\ngerar um primo de quantos bits? ", 8, 2048)
    inicio = time.time()
    p = gerar_primo(bits)
    print("  %d" % p)
    print("  gerado em %.3f s" % (time.time() - inicio))


if __name__ == "__main__":
    main()
