from missao1.securedocs_math.mdc import divisores

from . import cesar, afim, vigenere, fluxo
from .alfabeto import ALFABETO, so_letras, normalizar
from .frequencia import qui_quadrado, indice_coincidencia, ranking, ranking_portugues


def quebrar_cesar(cifrado):
    melhor = min(range(26), key=lambda k: qui_quadrado(cesar.decifrar(cifrado, k)))
    return melhor, cesar.decifrar(cifrado, melhor)


def ranking_cesar(cifrado, quantos=5):
    tentativas = [(qui_quadrado(cesar.decifrar(cifrado, k)), k) for k in range(26)]
    tentativas.sort()
    return [(k, q, cesar.decifrar(cifrado, k)) for q, k in tentativas[:quantos]]


def quebrar_afim(cifrado):
    melhor = min(afim.chaves_validas(), key=lambda ab: qui_quadrado(afim.decifrar(cifrado, *ab)))
    return melhor, afim.decifrar(cifrado, *melhor)


def ic_por_tamanho(cifrado, maximo=12):
    letras = so_letras(cifrado)
    resultado = []
    for m in range(1, maximo + 1):
        colunas = [letras[i::m] for i in range(m)]
        media = sum(indice_coincidencia(c) for c in colunas) / m
        resultado.append((m, media))
    return resultado


def tamanho_chave_vigenere(cifrado, maximo=12):
    tabela = ic_por_tamanho(cifrado, maximo)
    melhor = max(ic for _, ic in tabela)
    for m, ic in tabela:
        if ic >= 0.9 * melhor:
            return m


def kasiski(cifrado, tamanho=3, maximo=12):
    letras = so_letras(cifrado)
    vistos = {}
    distancias = []
    for i in range(len(letras) - tamanho + 1):
        trecho = letras[i:i + tamanho]
        if trecho in vistos:
            distancias.append((trecho, i - vistos[trecho]))
        vistos[trecho] = i
    votos = {m: 0 for m in range(2, maximo + 1)}
    for _, d in distancias:
        for m in divisores(d):
            if m in votos:
                votos[m] += 1
    return distancias, votos


def quebrar_vigenere(cifrado, tamanho=None):
    if tamanho is None:
        tamanho = tamanho_chave_vigenere(cifrado)
    letras = so_letras(cifrado)
    chave = ""
    for i in range(tamanho):
        k, _ = quebrar_cesar(letras[i::tamanho])
        chave += ALFABETO[k]
    for p in range(1, len(chave) + 1):
        if len(chave) % p == 0 and chave == chave[:p] * (len(chave) // p):
            chave = chave[:p]
            break
    return chave, vigenere.decifrar(cifrado, chave)


def chute_substituicao(cifrado):
    trocas = dict(zip(ranking(cifrado), ranking_portugues()))
    texto = "".join(trocas.get(c, c) for c in normalizar(cifrado))
    return trocas, texto


def letras_certas(tentativa, original):
    a, b = so_letras(tentativa), so_letras(original)
    certas = sum(1 for x, y in zip(a, b) if x == y)
    return certas, len(b)


def identificar_cifra(cifrado):
    ic = indice_coincidencia(cifrado)
    q = qui_quadrado(cifrado)
    if ic < 0.055:
        tipo = "polialfabética (Vigenère, Hill, fluxo...)"
    elif q < 60:
        tipo = "transposição ou texto claro (as letras são as do português)"
    else:
        tipo = "monoalfabética (César, afim, substituição...)"
    return ic, q, tipo


def quebrar_semente(cifrado, comeco_conhecido, bits=16):
    comeco = comeco_conhecido.encode("utf-8")
    for semente in range(2 ** bits):
        if fluxo.xor_bytes(cifrado[:len(comeco)], fluxo.gerar_fluxo(semente, len(comeco))) == comeco:
            return semente
    return None


def reuso_de_fluxo(cifrado1, cifrado2, claro1):
    p1 = claro1.encode("utf-8")
    p2 = fluxo.xor_bytes(fluxo.xor_bytes(cifrado1, cifrado2), p1)
    return p2.decode("utf-8", errors="replace")
