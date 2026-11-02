# Modos de operação: como usar uma cifra de bloco em mensagens de qualquer tamanho.
# Funcionam com qualquer objeto que tenha tamanho_bloco, cifrar_bloco e
# decifrar_bloco (DES, 3DES, RC5 e AES desta biblioteca).

from .blocos import xor_bytes, dividir_blocos, pkcs7_preencher, pkcs7_remover, chave_aleatoria


# ECB: cada bloco cifrado sozinho. Blocos iguais -> cifrados iguais (vaza padrão).
def cifrar_ecb(cifra, dados):
    n = cifra.tamanho_bloco
    return b"".join(cifra.cifrar_bloco(b) for b in dividir_blocos(pkcs7_preencher(dados, n), n))


def decifrar_ecb(cifra, cifrado):
    n = cifra.tamanho_bloco
    return pkcs7_remover(b"".join(cifra.decifrar_bloco(b) for b in dividir_blocos(cifrado, n)), n)


# CBC: C(i) = E(P(i) xor C(i-1)), com C(0) = IV aleatório.
# Blocos iguais viram cifrados diferentes; o mesmo arquivo cifrado duas vezes também.
def cifrar_cbc(cifra, dados, iv=None):
    n = cifra.tamanho_bloco
    if iv is None:
        iv = chave_aleatoria(n)
    anterior, saida = iv, []
    for bloco in dividir_blocos(pkcs7_preencher(dados, n), n):
        anterior = cifra.cifrar_bloco(xor_bytes(bloco, anterior))
        saida.append(anterior)
    return iv, b"".join(saida)


def decifrar_cbc(cifra, cifrado, iv):
    n = cifra.tamanho_bloco
    anterior, saida = iv, []
    for bloco in dividir_blocos(cifrado, n):
        saida.append(xor_bytes(cifra.decifrar_bloco(bloco), anterior))
        anterior = bloco
    return pkcs7_remover(b"".join(saida), n)


# CTR: transforma a cifra de bloco em cifra de fluxo (como na Missão 2):
# fluxo = E(nonce || 0), E(nonce || 1), ...  e  C = P xor fluxo.
# Não precisa de enchimento e cifrar = decifrar. O nonce nunca pode se repetir com a mesma chave.
def ctr(cifra, dados, nonce):
    n = cifra.tamanho_bloco
    tam_contador = n - len(nonce)
    saida = []
    for i, bloco in enumerate(dividir_blocos(dados, n)):
        fluxo = cifra.cifrar_bloco(nonce + i.to_bytes(tam_contador, "big"))
        saida.append(xor_bytes(bloco, fluxo))
    return b"".join(saida)


def cifrar_ctr(cifra, dados, nonce=None):
    if nonce is None:
        nonce = chave_aleatoria(cifra.tamanho_bloco // 2)
    return nonce, ctr(cifra, dados, nonce)


def decifrar_ctr(cifra, cifrado, nonce):
    return ctr(cifra, cifrado, nonce)
