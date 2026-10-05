from .alfabeto import so_letras


def ordem_colunas(palavra):
    palavra = so_letras(palavra)
    return sorted(range(len(palavra)), key=lambda i: (palavra[i], i))


def grade(texto, palavra):
    letras = so_letras(texto)
    n = len(so_letras(palavra))
    return [letras[i:i + n] for i in range(0, len(letras), n)]


def cifrar(texto, palavra):
    letras = so_letras(texto)
    n = len(so_letras(palavra))
    if n < 2:
        raise ValueError("a palavra-chave precisa ter pelo menos 2 letras")
    saida = ""
    for col in ordem_colunas(palavra):
        saida += letras[col::n]
    return saida


def decifrar(texto, palavra):
    letras = so_letras(texto)
    n = len(so_letras(palavra))
    linhas_cheias, sobra = divmod(len(letras), n)
    colunas = [""] * n
    pos = 0
    for col in ordem_colunas(palavra):
        tamanho = linhas_cheias + (1 if col < sobra else 0)
        colunas[col] = letras[pos:pos + tamanho]
        pos += tamanho
    saida = ""
    for i in range(linhas_cheias + 1):
        for col in range(n):
            if i < len(colunas[col]):
                saida += colunas[col][i]
    return saida


def cerca_cifrar(texto, trilhos):
    letras = so_letras(texto)
    linhas = [""] * trilhos
    for i, c in zip(_zigue_zague(len(letras), trilhos), letras):
        linhas[i] += c
    return "".join(linhas)


def cerca_decifrar(texto, trilhos):
    letras = so_letras(texto)
    caminho = list(_zigue_zague(len(letras), trilhos))
    quantos = [caminho.count(t) for t in range(trilhos)]
    linhas = []
    pos = 0
    for q in quantos:
        linhas.append(list(letras[pos:pos + q]))
        pos += q
    return "".join(linhas[t].pop(0) for t in caminho)


def _zigue_zague(tamanho, trilhos):
    if trilhos < 2:
        raise ValueError("precisa de pelo menos 2 trilhos")
    t, passo = 0, 1
    for _ in range(tamanho):
        yield t
        if t == 0:
            passo = 1
        elif t == trilhos - 1:
            passo = -1
        t += passo
