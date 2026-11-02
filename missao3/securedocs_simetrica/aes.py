# AES - Advanced Encryption Standard (FIPS 197, 2001; algoritmo Rijndael)
# rede de substituição-permutação: bloco de 128 bits, chave de 128/192/256 bits,
# 10/12/14 rodadas. Cada rodada: SubBytes, ShiftRows, MixColumns, AddRoundKey.
# Toda a conta é feita no corpo finito GF(2^8) = polinômios de grau < 8 mod
# m(x) = x^8 + x^4 + x^3 + x + 1 (0x11B).

TAMANHO_BLOCO = 16
RODADAS = {16: 10, 24: 12, 32: 14}
MODULO_GF = 0x11B


# ---------------------------------------------------------------- GF(2^8)
# soma é xor; multiplicar por x (xtime) é deslocar e, se passar de 8 bits,
# reduzir mod m(x) - igual à aritmética modular da Missão 1, só que com polinômios

def xtime(a):
    a <<= 1
    if a & 0x100:
        a ^= MODULO_GF
    return a


def mult_gf(a, b):
    resultado = 0
    while b:
        if b & 1:
            resultado ^= a
        a = xtime(a)
        b >>= 1
    return resultado


def potencia_gf(a, e):
    # mesma ideia do exp_mod da Missão 1 (quadrados sucessivos)
    resultado = 1
    while e:
        if e & 1:
            resultado = mult_gf(resultado, a)
        a = mult_gf(a, a)
        e >>= 1
    return resultado


def inverso_gf(a):
    # o grupo multiplicativo tem 255 elementos, então a^255 = 1 e a^-1 = a^254
    # (é o teorema de Fermat/Euler da Missão 1 aplicado em GF(2^8)); 0 vai para 0
    return potencia_gf(a, 254) if a else 0


def girar_8(b, n):
    return ((b << n) | (b >> (8 - n))) & 0xFF


def transformacao_afim(b):
    return b ^ girar_8(b, 1) ^ girar_8(b, 2) ^ girar_8(b, 3) ^ girar_8(b, 4) ^ 0x63


# a S-box não é uma tabela "mágica": é o inverso em GF(2^8) seguido de uma
# transformação afim. Aqui ela é calculada em vez de copiada.
SBOX = [transformacao_afim(inverso_gf(x)) for x in range(256)]
SBOX_INV = [0] * 256
for _x, _y in enumerate(SBOX):
    SBOX_INV[_y] = _x

# tabelas de multiplicação para o MixColumns (só acelera, a conta é mult_gf)
MULT = {n: [mult_gf(x, n) for x in range(256)] for n in (2, 3, 9, 11, 13, 14)}

RCON = [0, 1]
for _ in range(14):
    RCON.append(xtime(RCON[-1]))


# ---------------------------------------------------------------- expansão da chave

def expandir_chave(chave):
    if len(chave) not in RODADAS:
        raise ValueError("a chave do AES tem 16, 24 ou 32 bytes")
    nk = len(chave) // 4
    nr = RODADAS[len(chave)]
    w = [list(chave[4 * i:4 * i + 4]) for i in range(nk)]
    for i in range(nk, 4 * (nr + 1)):
        temp = list(w[i - 1])
        if i % nk == 0:
            temp = temp[1:] + temp[:1]                 # RotWord
            temp = [SBOX[b] for b in temp]             # SubWord
            temp[0] ^= RCON[i // nk]
        elif nk > 6 and i % nk == 4:
            temp = [SBOX[b] for b in temp]
        w.append([a ^ b for a, b in zip(w[i - nk], temp)])
    # cada chave de rodada são 4 palavras = 16 bytes
    return [bytes(sum(w[4 * r:4 * r + 4], [])) for r in range(nr + 1)]


# ---------------------------------------------------------------- etapas da rodada
# o estado é a matriz 4x4 de bytes guardada por colunas: estado[linha + 4 * coluna]

def sub_bytes(s):
    return [SBOX[b] for b in s]


def sub_bytes_inv(s):
    return [SBOX_INV[b] for b in s]


def shift_rows(s):
    # a linha r gira r posições para a esquerda
    return [s[r + 4 * ((c + r) % 4)] for c in range(4) for r in range(4)]


def shift_rows_inv(s):
    return [s[r + 4 * ((c - r) % 4)] for c in range(4) for r in range(4)]


def mix_columns(s):
    # cada coluna é multiplicada pela matriz [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
    m2, m3 = MULT[2], MULT[3]
    saida = []
    for c in range(4):
        a0, a1, a2, a3 = s[4 * c:4 * c + 4]
        saida += [m2[a0] ^ m3[a1] ^ a2 ^ a3,
                  a0 ^ m2[a1] ^ m3[a2] ^ a3,
                  a0 ^ a1 ^ m2[a2] ^ m3[a3],
                  m3[a0] ^ a1 ^ a2 ^ m2[a3]]
    return saida


def mix_columns_inv(s):
    # matriz inversa [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
    m9, m11, m13, m14 = MULT[9], MULT[11], MULT[13], MULT[14]
    saida = []
    for c in range(4):
        a0, a1, a2, a3 = s[4 * c:4 * c + 4]
        saida += [m14[a0] ^ m11[a1] ^ m13[a2] ^ m9[a3],
                  m9[a0] ^ m14[a1] ^ m11[a2] ^ m13[a3],
                  m13[a0] ^ m9[a1] ^ m14[a2] ^ m11[a3],
                  m11[a0] ^ m13[a1] ^ m9[a2] ^ m14[a3]]
    return saida


def add_round_key(s, k):
    return [a ^ b for a, b in zip(s, k)]


def matriz(estado):
    # para mostrar na tela: 4 linhas de 4 bytes
    return [" ".join("%02X" % estado[r + 4 * c] for c in range(4)) for r in range(4)]


class Cifra:
    nome = "AES"
    tamanho_bloco = TAMANHO_BLOCO

    def __init__(self, chave):
        self.chaves = expandir_chave(chave)
        self.rodadas = len(self.chaves) - 1
        self.nome = "AES-%d" % (8 * len(chave))

    def cifrar_bloco(self, bloco, passos=None):
        def anotar(rodada, etapa):
            if passos is not None:
                passos.append((rodada, etapa, bytes(s)))

        s = add_round_key(list(bloco), self.chaves[0])
        anotar(0, "AddRoundKey")
        for r in range(1, self.rodadas + 1):
            s = sub_bytes(s)
            anotar(r, "SubBytes")
            s = shift_rows(s)
            anotar(r, "ShiftRows")
            if r != self.rodadas:            # a última rodada não tem MixColumns
                s = mix_columns(s)
                anotar(r, "MixColumns")
            s = add_round_key(s, self.chaves[r])
            anotar(r, "AddRoundKey")
        return bytes(s)

    def decifrar_bloco(self, bloco):
        s = add_round_key(list(bloco), self.chaves[self.rodadas])
        for r in range(self.rodadas - 1, -1, -1):
            s = shift_rows_inv(s)
            s = sub_bytes_inv(s)
            s = add_round_key(s, self.chaves[r])
            if r != 0:
                s = mix_columns_inv(s)
        return bytes(s)


def cifrar_bloco(bloco, chave):
    return Cifra(chave).cifrar_bloco(bloco)


def decifrar_bloco(bloco, chave):
    return Cifra(chave).decifrar_bloco(bloco)
