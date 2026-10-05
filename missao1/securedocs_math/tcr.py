from .mdc import mdc
from .inverso_multiplicativo import inverso_multiplicativo


def _validar(restos, modulos):
    if len(restos) != len(modulos):
        raise ValueError("restos e módulos precisam ter o mesmo tamanho")
    if len(modulos) == 0:
        raise ValueError("informe pelo menos um módulo")
    for m in modulos:
        if m < 1:
            raise ValueError("módulos precisam ser positivos")
    for i in range(len(modulos)):
        for j in range(i + 1, len(modulos)):
            if mdc(modulos[i], modulos[j]) != 1:
                raise ValueError("módulos %d e %d não são coprimos" % (modulos[i], modulos[j]))


def tcr(restos, modulos):
    """Resolve x = a_i (mod n_i) e devolve (x, M), com M = produto dos módulos."""
    _validar(restos, modulos)
    M = 1
    for m in modulos:
        M *= m

    x = 0
    for a_i, n_i in zip(restos, modulos):
        if n_i == 1:
            continue
        M_i = M // n_i
        y_i = inverso_multiplicativo(M_i, n_i)
        x += a_i * M_i * y_i
    return x % M, M


def tcr_passos(restos, modulos):
    _validar(restos, modulos)
    M = 1
    for m in modulos:
        M *= m
    passos = ["M = %s = %d" % (" * ".join(str(m) for m in modulos), M)]
    x = 0
    termos = []
    for i, (a_i, n_i) in enumerate(zip(restos, modulos), 1):
        if n_i == 1:
            passos.append("  x = %d (mod 1): não restringe nada, parcela = 0" % a_i)
            continue
        M_i = M // n_i
        y_i = inverso_multiplicativo(M_i, n_i)
        passos.append("  M_%d = %d / %d = %d, y_%d = %d (inverso de %d mod %d)"
                      % (i, M, n_i, M_i, i, y_i, M_i, n_i))
        x += a_i * M_i * y_i
        termos.append((i, a_i, M_i, y_i))

    # x = a_1*M_1*y_1 + ... (mod M)
    passos.append("x = " + " + ".join("a_%d*M_%d*y_%d" % (i, i, i) for i, _, _, _ in termos))
    passos.append("  = " + " + ".join("%d*%d*%d" % (a, mi, yi) for _, a, mi, yi in termos))
    passos.append("  = %d  ->  x = %d (mod %d)" % (x, x % M, M))
    return passos


def decompor(x, modulos):
    return [x % m for m in modulos]
