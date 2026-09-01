from .euclides import euclides


def divisores(n):
    n = abs(n)
    if n == 0:
        raise ValueError("zero tem infinitos divisores")
    menores = []
    maiores = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            menores.append(d)
            if d != n // d:
                maiores.append(n // d)
        d += 1
    maiores.reverse()
    return menores + maiores


def mdc_ingenuo(a, b):
    """MDC pela definição, comparando as listas de divisores. Lento."""
    a, b = abs(a), abs(b)
    if a == 0:
        return b
    if b == 0:
        return a
    comuns = set(divisores(a)) & set(divisores(b))
    return max(comuns)


def mdc(a, b):
    return euclides(a, b)


def mmc(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // mdc(a, b)


def coprimos(a, b):
    return mdc(a, b) == 1
