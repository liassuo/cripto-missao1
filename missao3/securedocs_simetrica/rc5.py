# RC5 (Rivest, 1994) - RC5-w/r/b
#   w = tamanho da palavra em bits (16, 32 ou 64) -> bloco de 2w bits
#   r = número de rodadas (0 a 255)
#   b = tamanho da chave em bytes (0 a 255)
# Só usa três operações: soma mod 2^w, xor e rotação dependente dos dados.
# O padrão sugerido é RC5-32/12/16 (bloco de 64 bits, 12 rodadas, chave de 128 bits).

# P = Odd((e - 2) * 2^w)   e   Q = Odd((phi - 1) * 2^w), phi = razão áurea
CONSTANTES = {
    16: (0xB7E1, 0x9E37),
    32: (0xB7E15163, 0x9E3779B9),
    64: (0xB7E151628AED2A6B, 0x9E3779B97F4A7C15),
}


def girar_esq(x, n, w):
    n %= w
    mascara = (1 << w) - 1
    return ((x << n) | (x >> (w - n))) & mascara


def girar_dir(x, n, w):
    n %= w
    mascara = (1 << w) - 1
    return ((x >> n) | (x << (w - n))) & mascara


def expandir_chave(chave, w=32, r=12):
    if w not in CONSTANTES:
        raise ValueError("w precisa ser 16, 32 ou 64")
    if len(chave) > 255 or not 0 <= r <= 255:
        raise ValueError("chave até 255 bytes e até 255 rodadas")
    u = w // 8
    mascara = (1 << w) - 1
    p, q = CONSTANTES[w]

    # 1. a chave vira c palavras L (little-endian)
    c = max(1, -(-len(chave) // u))
    chave_completa = chave + bytes(c * u - len(chave))
    L = [int.from_bytes(chave_completa[i * u:(i + 1) * u], "little") for i in range(c)]

    # 2. tabela S com t = 2(r + 1) palavras, iniciada com as constantes mágicas
    t = 2 * (r + 1)
    S = [(p + i * q) & mascara for i in range(t)]

    # 3. mistura L dentro de S, 3 * max(t, c) vezes
    a = b = i = j = 0
    for _ in range(3 * max(t, c)):
        a = S[i] = girar_esq((S[i] + a + b) & mascara, 3, w)
        b = L[j] = girar_esq((L[j] + a + b) & mascara, a + b, w)
        i = (i + 1) % t
        j = (j + 1) % c
    return S


class Cifra:
    def __init__(self, chave, w=32, r=12):
        self.w, self.r = w, r
        self.u = w // 8
        self.tamanho_bloco = 2 * self.u
        self.mascara = (1 << w) - 1
        self.S = expandir_chave(chave, w, r)
        self.nome = "RC5-%d/%d/%d" % (w, r, len(chave))

    def _palavras(self, bloco):
        if len(bloco) != self.tamanho_bloco:
            raise ValueError("o bloco do RC5-%d tem %d bytes" % (self.w, self.tamanho_bloco))
        u = self.u
        return int.from_bytes(bloco[:u], "little"), int.from_bytes(bloco[u:], "little")

    def _juntar(self, a, b):
        return a.to_bytes(self.u, "little") + b.to_bytes(self.u, "little")

    def cifrar_bloco(self, bloco, passos=None):
        S, w, m = self.S, self.w, self.mascara
        a, b = self._palavras(bloco)
        a = (a + S[0]) & m
        b = (b + S[1]) & m
        for i in range(1, self.r + 1):
            # rotação que depende do próprio dado: é o que dá a força do RC5
            a = (girar_esq(a ^ b, b, w) + S[2 * i]) & m
            b = (girar_esq(b ^ a, a, w) + S[2 * i + 1]) & m
            if passos is not None:
                passos.append((i, a, b))
        return self._juntar(a, b)

    def decifrar_bloco(self, bloco):
        S, w, m = self.S, self.w, self.mascara
        a, b = self._palavras(bloco)
        for i in range(self.r, 0, -1):
            b = girar_dir((b - S[2 * i + 1]) & m, a, w) ^ a
            a = girar_dir((a - S[2 * i]) & m, b, w) ^ b
        b = (b - S[1]) & m
        a = (a - S[0]) & m
        return self._juntar(a, b)


def cifrar_bloco(bloco, chave, w=32, r=12):
    return Cifra(chave, w, r).cifrar_bloco(bloco)


def decifrar_bloco(bloco, chave, w=32, r=12):
    return Cifra(chave, w, r).decifrar_bloco(bloco)
