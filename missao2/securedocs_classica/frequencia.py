from .alfabeto import ALFABETO, so_letras

FREQ_PORTUGUES = {
    "A": 14.63, "B": 1.04, "C": 3.88, "D": 4.99, "E": 12.57, "F": 1.02,
    "G": 1.30, "H": 1.28, "I": 6.18, "J": 0.40, "K": 0.02, "L": 2.78,
    "M": 4.74, "N": 5.05, "O": 10.73, "P": 2.52, "Q": 1.20, "R": 6.53,
    "S": 7.81, "T": 4.34, "U": 4.63, "V": 1.67, "W": 0.01, "X": 0.21,
    "Y": 0.01, "Z": 0.47,
}

IC_PORTUGUES = sum((f / 100) ** 2 for f in FREQ_PORTUGUES.values())
IC_ALEATORIO = 1 / 26


def contar_letras(texto):
    contagem = {c: 0 for c in ALFABETO}
    for c in so_letras(texto):
        contagem[c] += 1
    return contagem


def frequencias(texto):
    contagem = contar_letras(texto)
    total = sum(contagem.values())
    if total == 0:
        return {c: 0.0 for c in ALFABETO}
    return {c: 100.0 * contagem[c] / total for c in ALFABETO}


def ranking(texto):
    contagem = contar_letras(texto)
    return sorted(ALFABETO, key=lambda c: (-contagem[c], c))


def ranking_portugues():
    return sorted(ALFABETO, key=lambda c: -FREQ_PORTUGUES[c])


def indice_coincidencia(texto):
    contagem = contar_letras(texto)
    n = sum(contagem.values())
    if n < 2:
        return 0.0
    return sum(f * (f - 1) for f in contagem.values()) / (n * (n - 1))


def qui_quadrado(texto):
    contagem = contar_letras(texto)
    n = sum(contagem.values())
    if n == 0:
        return float("inf")
    total = 0.0
    for c in ALFABETO:
        esperado = n * FREQ_PORTUGUES[c] / 100
        total += (contagem[c] - esperado) ** 2 / esperado
    return total


def histograma(texto, largura=40):
    freq = frequencias(texto)
    maior = max(freq.values()) or 1
    linhas = []
    for c in ALFABETO:
        barra = "#" * int(round(largura * freq[c] / maior))
        linhas.append("  %s %5.1f%% %s" % (c, freq[c], barra))
    return linhas
