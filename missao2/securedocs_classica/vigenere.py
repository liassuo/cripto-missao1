from missao1.securedocs_math.aritmetica_modular import mod

from .alfabeto import N, normalizar, so_letras, eh_letra, letra_para_numero, numero_para_letra


def _aplicar(texto, chave, sinal):
    deslocamentos = [letra_para_numero(c) for c in so_letras(chave)]
    if not deslocamentos:
        raise ValueError("a chave precisa ter pelo menos uma letra")
    saida = []
    i = 0
    for c in normalizar(texto):
        if eh_letra(c):
            k = deslocamentos[i % len(deslocamentos)]
            saida.append(numero_para_letra(mod(letra_para_numero(c) + sinal * k, N)))
            i += 1
        else:
            saida.append(c)
    return "".join(saida)


def cifrar(texto, chave):
    return _aplicar(texto, chave, 1)


def decifrar(texto, chave):
    return _aplicar(texto, chave, -1)


def tabela_passos(texto, chave):
    claro = so_letras(texto)
    k = so_letras(chave)
    chave_repetida = "".join(k[i % len(k)] for i in range(len(claro)))
    cifrado = so_letras(cifrar(claro, k))
    return ["texto  : " + claro,
            "chave  : " + chave_repetida,
            "cifrado: " + cifrado]
