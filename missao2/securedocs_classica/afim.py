from missao1.securedocs_math.mdc import coprimos
from missao1.securedocs_math.inverso_multiplicativo import inverso_multiplicativo
from missao1.securedocs_math.aritmetica_modular import mod

from .alfabeto import N, normalizar, eh_letra, letra_para_numero, numero_para_letra


def chave_valida(a):
    return coprimos(a, N)


def chaves_validas():
    return [(a, b) for a in range(1, N) if coprimos(a, N) for b in range(N)]


def cifrar(texto, a, b):
    # C = (a*P + b) mod 26
    if not chave_valida(a):
        raise ValueError("a = %d não é coprimo com 26, não teria como decifrar" % a)
    saida = []
    for c in normalizar(texto):
        if eh_letra(c):
            p = letra_para_numero(c)
            saida.append(numero_para_letra(mod(a * p + b, N)))
        else:
            saida.append(c)
    return "".join(saida)


def decifrar(texto, a, b):
    a_inv = inverso_multiplicativo(a, N)
    saida = []
    for c in normalizar(texto):
        if eh_letra(c):
            x = letra_para_numero(c)
            saida.append(numero_para_letra(mod(a_inv * (x - b), N)))
        else:
            saida.append(c)
    return "".join(saida)


def forca_bruta(cifrado):
    return [((a, b), decifrar(cifrado, a, b)) for a, b in chaves_validas()]
