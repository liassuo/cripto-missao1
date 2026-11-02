import time

from . import des, aes, rc5
from .blocos import chave_aleatoria, bits_diferentes, inverter_bit

CARACTERISTICAS = [
    # algoritmo, ano, autores, estrutura, bloco, chave, rodadas, situação hoje
    ("DES", 1977, "IBM / NBS (FIPS 46)", "Feistel", "64", "56", "16",
     "quebrado por força bruta (1998); retirado pelo NIST em 2005"),
    ("3DES", 1998, "ANSI X9.52 / NIST", "Feistel (3 x DES)", "64", "112 ou 168", "48",
     "lento e bloco pequeno (Sweet32); proibido pelo NIST desde 2024"),
    ("RC5", 1994, "Ronald Rivest (RSA)", "Feistel modificada (ARX)", "32, 64 ou 128", "0 a 2040",
     "0 a 255 (12 sugerido)", "sem padrão oficial; 12 rodadas vulneráveis a criptoanálise diferencial teórica"),
    ("AES", 2001, "Daemen e Rijmen (FIPS 197)", "substituição-permutação", "128",
     "128, 192 ou 256", "10, 12 ou 14", "padrão mundial; sem ataque prático conhecido"),
]

# bits efetivos de segurança contra força bruta
BITS_EFETIVOS = [("DES", 56), ("3DES (2 chaves)", 80), ("3DES (3 chaves)", 112),
                 ("RC5-32/12/16", 128), ("AES-128", 128), ("AES-256", 256)]

SEGUNDOS_POR_ANO = 365.25 * 24 * 3600


def tempo_forca_bruta(bits, chaves_por_segundo):
    # em média o atacante acerta depois de testar metade das chaves
    return 2 ** (bits - 1) / chaves_por_segundo


def formatar_tempo(segundos):
    if segundos < 60:
        return "%.1f segundos" % segundos
    if segundos < 3600:
        return "%.1f minutos" % (segundos / 60)
    if segundos < 86400:
        return "%.1f horas" % (segundos / 3600)
    anos = segundos / SEGUNDOS_POR_ANO
    if anos < 1:
        return "%.1f dias" % (segundos / 86400)
    if anos < 1e6:
        return "%.0f anos" % anos
    return "%.1e anos" % anos


def cifras_padrao():
    # chaves aleatórias nos tamanhos usuais de cada algoritmo
    return [
        des.Cifra(chave_aleatoria(8)),
        des.CifraTripla(chave_aleatoria(24)),
        rc5.Cifra(chave_aleatoria(16)),
        aes.Cifra(chave_aleatoria(16)),
        aes.Cifra(chave_aleatoria(32)),
    ]


def medir_velocidade(cifra, n_bytes=8192):
    n = cifra.tamanho_bloco
    bloco = bytes(n)
    blocos = max(1, n_bytes // n)
    inicio = time.perf_counter()
    for _ in range(blocos):
        bloco = cifra.cifrar_bloco(bloco)
    duracao = time.perf_counter() - inicio
    return blocos * n / duracao


def avalanche(cifra, bloco, bit=0):
    # troca 1 bit do texto claro e conta quantos bits do cifrado mudaram
    c1 = cifra.cifrar_bloco(bloco)
    c2 = cifra.cifrar_bloco(inverter_bit(bloco, bit))
    return bits_diferentes(c1, c2), 8 * len(c1)


def avalanche_medio(cifra, amostras=64):
    n = cifra.tamanho_bloco
    total = 0
    for i in range(amostras):
        bloco = chave_aleatoria(n)
        mudou, tamanho = avalanche(cifra, bloco, i % (8 * n))
        total += mudou
    return total / amostras, 8 * n
