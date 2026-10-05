import unicodedata

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N = 26


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return sem_acento.upper()


def so_letras(texto):
    return "".join(c for c in normalizar(texto) if c in ALFABETO)


def eh_letra(c):
    return c in ALFABETO


def letra_para_numero(c):
    return ALFABETO.index(c)


def numero_para_letra(x):
    return ALFABETO[x % N]


def texto_para_numeros(texto):
    return [letra_para_numero(c) for c in so_letras(texto)]


def numeros_para_texto(numeros):
    return "".join(numero_para_letra(x) for x in numeros)


def agrupar(texto, tamanho=5):
    return " ".join(texto[i:i + tamanho] for i in range(0, len(texto), tamanho))
