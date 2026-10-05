from missao1.securedocs_math.aritmetica_modular import mod

from .alfabeto import N, normalizar, eh_letra, letra_para_numero, numero_para_letra


def deslocar(texto, k):
    saida = []
    for c in normalizar(texto):
        if eh_letra(c):
            saida.append(numero_para_letra(mod(letra_para_numero(c) + k, N)))
        else:
            saida.append(c)
    return "".join(saida)


def cifrar(texto, k):
    # C = (P + k) mod 26
    return deslocar(texto, k)


def decifrar(texto, k):
    # P = (C - k) mod 26
    return deslocar(texto, -k)


def forca_bruta(cifrado):
    return [(k, decifrar(cifrado, k)) for k in range(1, N)]
