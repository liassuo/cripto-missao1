import secrets

from missao1.securedocs_math.aritmetica_modular import mod, soma_mod, mult_mod

from .alfabeto import N, texto_para_numeros, numeros_para_texto, ALFABETO


def chave_vernam(tamanho):
    return "".join(ALFABETO[secrets.randbelow(N)] for _ in range(tamanho))


def vernam_cifrar(texto, chave):
    p = texto_para_numeros(texto)
    k = texto_para_numeros(chave)
    if len(k) < len(p):
        raise ValueError("no one-time pad a chave precisa ser do tamanho da mensagem")
    return numeros_para_texto(soma_mod(a, b, N) for a, b in zip(p, k))


def vernam_decifrar(texto, chave):
    c = texto_para_numeros(texto)
    k = texto_para_numeros(chave)
    return numeros_para_texto(mod(a - b, N) for a, b in zip(c, k))


LCG_A = 1103515245
LCG_C = 12345
LCG_M = 2 ** 31


def gerar_fluxo(semente, tamanho):
    x = mod(semente, LCG_M)
    fluxo = []
    for _ in range(tamanho):
        x = soma_mod(mult_mod(LCG_A, x, LCG_M), LCG_C, LCG_M)
        fluxo.append((x >> 16) & 0xFF)
    return bytes(fluxo)


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def cifrar(texto, semente):
    dados = texto.encode("utf-8") if isinstance(texto, str) else texto
    return xor_bytes(dados, gerar_fluxo(semente, len(dados)))


def decifrar(cifrado, semente):
    return xor_bytes(cifrado, gerar_fluxo(semente, len(cifrado))).decode("utf-8", errors="replace")


def para_hex(dados):
    return dados.hex().upper()
