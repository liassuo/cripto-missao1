from .euclides_estendido import euclides_estendido
from .mdc import mdc


def inverso_multiplicativo(a, n):
    """x tal que a*x = 1 (mod n). Vem do a*x + n*y = 1 do Euclides estendido."""
    n = abs(n)
    if n <= 1:
        raise ValueError("módulo precisa ser maior que 1")
    g, x, y = euclides_estendido(a % n, n)
    if g != 1:
        raise ValueError("%d não tem inverso mod %d (mdc = %d)" % (a, n, g))
    return x % n


def tem_inverso(a, n):
    return abs(n) > 1 and mdc(a, n) == 1


def inverso_forca_bruta(a, n):
    a = a % n
    for x in range(1, n):
        if (a * x) % n == 1:
            return x
    return None


def inverso_passos(a, n):
    passos = ["Inverso de %d módulo %d:" % (a, n)]
    g, x, y = euclides_estendido(a % n, n)
    passos.append("  Euclides estendido: %d*(%d) + %d*(%d) = %d" % (a, x, n, y, g))
    if g != 1:
        passos.append("  mdc = %d, diferente de 1 -> %d NÃO tem inverso mod %d" % (g, a, n))
        return passos
    inv = x % n
    passos.append("  então %d*(%d) = 1 (mod %d), e x mod %d = %d" % (a, x, n, n, inv))
    passos.append("  conferindo: %d * %d = %d = %d (mod %d)" % (a, inv, a * inv, (a * inv) % n, n))
    return passos
