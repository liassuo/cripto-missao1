from missao1.securedocs_math.mdc import coprimos
from missao1.securedocs_math.inverso_multiplicativo import inverso_multiplicativo
from missao1.securedocs_math.aritmetica_modular import mod

from .alfabeto import N, so_letras, texto_para_numeros, numeros_para_texto


def menor(m, i, j):
    return [linha[:j] + linha[j + 1:] for k, linha in enumerate(m) if k != i]


def determinante(m):
    if len(m) == 1:
        return m[0][0]
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    total = 0
    for j in range(len(m)):
        sinal = 1 if j % 2 == 0 else -1
        total += sinal * m[0][j] * determinante(menor(m, 0, j))
    return total


def multiplicar(a, b, n=N):
    linhas, meio, colunas = len(a), len(b), len(b[0])
    return [[mod(sum(a[i][k] * b[k][j] for k in range(meio)), n) for j in range(colunas)]
            for i in range(linhas)]


def chave_valida(k):
    return coprimos(mod(determinante(k), N), N)


def inversa(k):
    det = mod(determinante(k), N)
    if not coprimos(det, N):
        raise ValueError("det = %d não é coprimo com 26, a matriz não tem inversa" % det)
    det_inv = inverso_multiplicativo(det, N)
    n = len(k)
    if n == 1:
        return [[det_inv]]
    # adjunta = transposta da matriz dos cofatores
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            sinal = 1 if (i + j) % 2 == 0 else -1
            adj[j][i] = sinal * determinante(menor(k, i, j))
    return [[mod(det_inv * adj[i][j], N) for j in range(n)] for i in range(n)]


def _aplicar(numeros, k):
    n = len(k)
    saida = []
    for i in range(0, len(numeros), n):
        bloco = [[x] for x in numeros[i:i + n]]
        saida.extend(linha[0] for linha in multiplicar(k, bloco))
    return saida


def cifrar(texto, k, enchimento="X"):
    if not chave_valida(k):
        raise ValueError("matriz chave não é inversível mod 26")
    letras = so_letras(texto)
    while len(letras) % len(k) != 0:
        letras += enchimento
    return numeros_para_texto(_aplicar(texto_para_numeros(letras), k))


def decifrar(texto, k):
    return numeros_para_texto(_aplicar(texto_para_numeros(texto), inversa(k)))


def ataque_texto_conhecido(claro, cifrado):
    p = texto_para_numeros(claro)
    c = texto_para_numeros(cifrado)
    blocos = min(len(p), len(c)) // 2
    for i in range(blocos):
        for j in range(i + 1, blocos):
            mp = [[p[2 * i], p[2 * j]], [p[2 * i + 1], p[2 * j + 1]]]
            mc = [[c[2 * i], c[2 * j]], [c[2 * i + 1], c[2 * j + 1]]]
            if chave_valida(mp):
                return multiplicar(mc, inversa(mp))
    return None
