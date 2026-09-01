import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entrada import ler_int
from securedocs_math.mdc import coprimos
from securedocs_math.phi_euler import (phi, phi_contagem, phi_de_primos, phi_ate,
                                       teorema_euler, pequeno_teorema_fermat, carmichael)


def main():
    print("=== 7. FUNÇÃO PHI DE EULER ===\n")

    print("contando x fórmula:")
    for n in (10, 36, 97, 3120):
        print("  phi(%d) = %d (contagem) = %d (fórmula)" % (n, phi_contagem(n), phi(n)))
    print("  coprimos com 10:", [k for k in range(1, 11) if coprimos(k, 10)])

    print("\ncasos do RSA:")
    print("  phi(97) = 96 (primo: p-1)")
    print("  phi(61*53) =", phi_de_primos(61, 53), "= (61-1)*(53-1)")

    print("\ntabela phi(1..20):")
    tabela = phi_ate(20)
    print("  n  :", " ".join("%2d" % n for n in range(1, 21)))
    print("  phi:", " ".join("%2d" % tabela[n] for n in range(1, 21)))

    print("\nteorema de Euler: a^phi(n) = 1 (mod n)")
    print("  7^12 mod 36 == 1?", teorema_euler(7, 36))
    print("  Fermat: 7^12 mod 13 == 1?", pequeno_teorema_fermat(7, 13))

    print("\npor que o RSA fecha o ciclo:")
    p, q, e = 61, 53, 17
    n = p * q
    phi_n = phi_de_primos(p, q)
    d = pow(e, -1, phi_n)
    print("  e*d = %d*%d = %d = 1 + %d*phi(n)" % (e, d, e * d, (e * d - 1) // phi_n))
    print("  m^(e*d) mod n com m=65:", pow(65, e * d, n), "-> voltou o m")

    print("\nlambda de Carmichael:")
    print("  lambda(3120) =", carmichael(3120), "| phi(3120) =", phi(3120))


def interativo():
    n = ler_int("n = ", 1)

    print()
    print("  phi(%d) = %d" % (n, phi(n)))
    if n <= 5000:
        print("  conferindo pela contagem: %d" % phi_contagem(n))
        lista = [k for k in range(1, n + 1) if coprimos(k, n)]
        if len(lista) <= 30:
            print("  coprimos com %d: %s" % (n, lista))
    print("  lambda de Carmichael = %d" % carmichael(n))

    a = ler_int("\na para testar o teorema de Euler = ", 1)
    if coprimos(a, n):
        print("  %d^phi(%d) mod %d = 1? %s" % (a, n, n, teorema_euler(a, n)))
    else:
        print("  %d não é coprimo com %d, o teorema não se aplica" % (a, n))


if __name__ == "__main__":
    main()
