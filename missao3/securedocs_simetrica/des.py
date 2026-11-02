# DES - Data Encryption Standard (FIPS 46-3, 1977)
# cifra de Feistel: bloco de 64 bits, chave de 64 bits (56 úteis + 8 de paridade),
# 16 rodadas. Cada rodada: L(i) = R(i-1)  e  R(i) = L(i-1) xor f(R(i-1), K(i))

from .blocos import bytes_para_int, int_para_bytes

TAMANHO_BLOCO = 8
RODADAS = 16

# permutação inicial; a final é a inversa dela
IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

FP = [0] * 64
for _i, _p in enumerate(IP):
    FP[_p - 1] = _i + 1

# expansão de 32 para 48 bits (repete os bits das bordas de cada grupo de 4)
E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

# permutação depois das S-boxes
P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

# escolha permutada 1: tira os bits de paridade (8, 16, ..., 64) e embaralha
PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

# escolha permutada 2: escolhe 48 dos 56 bits para a subchave da rodada
PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

DESLOCAMENTOS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# S-boxes: a única parte não linear do DES. 6 bits entram, 4 saem.
# linha = bits 1 e 6, coluna = bits 2 a 5
SBOX = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]],
]


def permutar(valor, tabela, bits_entrada):
    # as tabelas do padrão contam as posições a partir de 1, da esquerda
    saida = 0
    for posicao in tabela:
        saida = (saida << 1) | ((valor >> (bits_entrada - posicao)) & 1)
    return saida


def girar_28(x, n):
    return ((x << n) | (x >> (28 - n))) & 0xFFFFFFF


def subchaves(chave):
    if len(chave) != 8:
        raise ValueError("a chave do DES tem 8 bytes (64 bits, 56 úteis)")
    k56 = permutar(bytes_para_int(chave), PC1, 64)
    c, d = k56 >> 28, k56 & 0xFFFFFFF
    saida = []
    for desloc in DESLOCAMENTOS:
        c, d = girar_28(c, desloc), girar_28(d, desloc)
        saida.append(permutar((c << 28) | d, PC2, 56))
    return saida


def aplicar_sboxes(x48):
    saida = 0
    for i in range(8):
        seis = (x48 >> (42 - 6 * i)) & 0x3F
        linha = ((seis >> 4) & 0b10) | (seis & 1)
        coluna = (seis >> 1) & 0xF
        saida = (saida << 4) | SBOX[i][linha][coluna]
    return saida


def funcao_f(r, k):
    # expande, mistura com a subchave, passa nas S-boxes e permuta
    x = permutar(r, E, 32) ^ k
    return permutar(aplicar_sboxes(x), P, 32)


def processar_bloco(bloco, chaves, passos=None):
    x = permutar(bytes_para_int(bloco), IP, 64)
    esq, dir_ = x >> 32, x & 0xFFFFFFFF
    for i, k in enumerate(chaves, 1):
        esq, dir_ = dir_, esq ^ funcao_f(dir_, k)
        if passos is not None:
            passos.append((i, esq, dir_, k))
    # na última rodada as metades não são trocadas: junta R16 L16
    return int_para_bytes(permutar((dir_ << 32) | esq, FP, 64), 8)


class Cifra:
    nome = "DES"
    tamanho_bloco = TAMANHO_BLOCO

    def __init__(self, chave):
        self.chaves = subchaves(chave)

    def cifrar_bloco(self, bloco, passos=None):
        return processar_bloco(bloco, self.chaves, passos)

    def decifrar_bloco(self, bloco, passos=None):
        # Feistel: decifrar é o mesmo circuito com as subchaves na ordem inversa
        return processar_bloco(bloco, self.chaves[::-1], passos)


class CifraTripla:
    # 3DES (EDE): C = E_K3(D_K2(E_K1(P))). Com K1 = K2 = K3 vira o DES comum.
    nome = "3DES"
    tamanho_bloco = TAMANHO_BLOCO

    def __init__(self, chave):
        if len(chave) == 16:
            chave = chave + chave[:8]       # opção 2: K3 = K1 (112 bits)
        if len(chave) != 24:
            raise ValueError("a chave do 3DES tem 16 ou 24 bytes")
        self.k1, self.k2, self.k3 = (Cifra(chave[i:i + 8]) for i in (0, 8, 16))

    def cifrar_bloco(self, bloco):
        return self.k3.cifrar_bloco(self.k2.decifrar_bloco(self.k1.cifrar_bloco(bloco)))

    def decifrar_bloco(self, bloco):
        return self.k1.decifrar_bloco(self.k2.cifrar_bloco(self.k3.decifrar_bloco(bloco)))


def cifrar_bloco(bloco, chave):
    return Cifra(chave).cifrar_bloco(bloco)


def decifrar_bloco(bloco, chave):
    return Cifra(chave).decifrar_bloco(bloco)


def chave_com_paridade(chave):
    # cada byte tem um número ímpar de bits 1 (o bit menos significativo ajusta)
    return bytes((b & 0xFE) | (bin(b >> 1).count("1") % 2 == 0) for b in chave)


# chaves fracas: geram 16 subchaves iguais, então cifrar duas vezes devolve o texto
CHAVES_FRACAS = ["0101010101010101", "FEFEFEFEFEFEFEFE", "E0E0E0E0F1F1F1F1", "1F1F1F1F0E0E0E0E"]
