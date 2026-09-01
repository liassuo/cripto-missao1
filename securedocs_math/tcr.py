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
    """Resolve x = a_i (mod n_i) e devolve (x, N), com N = produto dos módulos."""
    _validar(restos, modulos)
    N = 1
    for m in modulos:
        N *= m

    x = 0
    for a_i, n_i in zip(restos, modulos):
        if n_i == 1:
            continue
        N_i = N // n_i
        M_i = inverso_multiplicativo(N_i, n_i)
        x += a_i * N_i * M_i
    return x % N, N


def tcr_passos(restos, modulos):
    _validar(restos, modulos)
    N = 1
    for m in modulos:
        N *= m
    passos = ["Sistema com %d congruências, N = %d" % (len(modulos), N)]
    x = 0
    for a_i, n_i in zip(restos, modulos):
        if n_i == 1:
            passos.append("  x = %d (mod 1): não restringe nada, parcela = 0" % a_i)
            continue
        N_i = N // n_i
        M_i = inverso_multiplicativo(N_i, n_i)
        parcela = a_i * N_i * M_i
        passos.append("  x = %d (mod %d): N_i = %d, M_i = %d, parcela = %d" % (a_i, n_i, N_i, M_i, parcela))
        x += parcela
    passos.append("Soma = %d  ->  x = %d (mod %d)" % (x, x % N, N))
    return passos


def decompor(x, modulos):
    return [x % m for m in modulos]
