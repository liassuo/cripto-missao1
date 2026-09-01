def euclides_estendido(a, b):
    """Retorna (g, x, y) com a*x + b*y = g = mdc(a, b)."""
    r0, r1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    # a cada volta continua valendo a*x0 + b*y0 = r0
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    if r0 < 0:
        r0, x0, y0 = -r0, -x0, -y0
    return r0, x0, y0


def euclides_estendido_passos(a, b):
    passos = ["Euclides estendido para a=%d, b=%d" % (a, b), "  r0 | r1 | q | x | y"]
    r0, r1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        passos.append("  %d | %d | %d | %d | %d" % (r0, r1, q, x0, y0))
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    passos.append("Bezout: %d*(%d) + %d*(%d) = %d" % (a, x0, b, y0, r0))
    return passos
