import math
import secrets

from .alfabeto import ALFABETO, N, normalizar, so_letras


def chave_aleatoria():
    letras = list(ALFABETO)
    # Fisher-Yates
    for i in range(N - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        letras[i], letras[j] = letras[j], letras[i]
    return "".join(letras)


def chave_por_palavra(palavra):
    chave = ""
    for c in so_letras(palavra) + ALFABETO:
        if c not in chave:
            chave += c
    return chave


def chave_valida(chave):
    return len(chave) == N and sorted(chave) == list(ALFABETO)


def inverter_chave(chave):
    inversa = [""] * N
    for i, c in enumerate(chave):
        inversa[ALFABETO.index(c)] = ALFABETO[i]
    return "".join(inversa)


def _trocar(texto, de, para):
    tabela = dict(zip(de, para))
    return "".join(tabela.get(c, c) for c in normalizar(texto))


def cifrar(texto, chave):
    if not chave_valida(chave):
        raise ValueError("a chave precisa ter as 26 letras, cada uma uma vez")
    return _trocar(texto, ALFABETO, chave)


def decifrar(texto, chave):
    if not chave_valida(chave):
        raise ValueError("a chave precisa ter as 26 letras, cada uma uma vez")
    return _trocar(texto, chave, ALFABETO)


def tamanho_espaco_chaves():
    return math.factorial(N)
