def euclides(a, b):
    """mdc(a, b) = mdc(b, a mod b), até o resto dar zero."""
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def euclides_recursivo(a, b):
    a, b = abs(a), abs(b)
    if b == 0:
        return a
    return euclides_recursivo(b, a % b)


def euclides_passos(a, b):
    passos = ["mdc(%d, %d) pelo algoritmo de Euclides:" % (a, b)]
    a, b = abs(a), abs(b)
    while b != 0:
        q = a // b
        r = a % b
        passos.append("  %d = %d * %d + %d" % (a, b, q, r))
        a, b = b, r
    passos.append("Último resto não nulo -> MDC = %d" % a)
    return passos
