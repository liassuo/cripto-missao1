import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int
from securedocs_math.euclides_estendido import euclides_estendido, euclides_estendido_passos


def main():
    print("=== 4. EUCLIDES ESTENDIDO ===\n")

    print("tabela:")
    for linha in euclides_estendido_passos(240, 46):
        print("  " + linha)

    print("\nconferindo:")
    g, x, y = euclides_estendido(240, 46)
    print("  (g, x, y) =", (g, x, y))
    print("  240*(%d) + 46*(%d) = %d" % (x, y, 240 * x + 46 * y))

    print("\nquando o mdc é 1, o x já é o inverso (próxima demo):")
    g, x, y = euclides_estendido(17, 3120)
    print("  17*(%d) + 3120*(%d) = %d" % (x, y, g))
    print("  então 17 *", x % 3120, "= 1 (mod 3120) -> conferindo:", (17 * x) % 3120)


def interativo():
    a = ler_int("a = ", 1)
    b = ler_int("b = ", 1)

    print()
    for linha in euclides_estendido_passos(a, b):
        print("  " + linha)

    g, x, y = euclides_estendido(a, b)
    print("\n  conferindo: %d*(%d) + %d*(%d) = %d" % (a, x, b, y, a * x + b * y))
    if g == 1:
        print("  como o mdc é 1, %d é o inverso de %d mod %d" % (x % b, a, b))


if __name__ == "__main__":
    main()
