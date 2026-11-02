# Nova descoberta da missão: como entregar a chave secreta ao destinatário
# sem que um invasor também consiga obtê-la?
# Tudo aqui reaproveita a teoria dos números da Missão 1.

import hashlib
import secrets

from missao1.securedocs_math.exponenciacao_modular import exp_mod
from missao1.securedocs_math.inverso_multiplicativo import inverso_multiplicativo
from missao1.securedocs_math.primos import gerar_primo
from missao1.securedocs_math.mdc import coprimos


def chaves_necessarias(usuarios):
    # com chave simétrica, cada par de usuários precisa da sua chave: n(n - 1)/2
    return usuarios * (usuarios - 1) // 2


# ---------------------------------------------------------------- Diffie-Hellman (1976)
# públicos: primo p e gerador g. Alice sorteia a e manda A = g^a mod p,
# Bob sorteia b e manda B = g^b mod p. Os dois chegam a g^(ab) mod p:
#   Alice: B^a = g^(ba)      Bob: A^b = g^(ab)
# O invasor vê p, g, A e B, mas para achar a precisaria resolver o logaritmo discreto.

# grupo 14 da RFC 3526: primo seguro de 2048 bits, gerador 2
P_2048 = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74"
    "020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F1437"
    "4FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF05"
    "98DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB"
    "9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF695581718"
    "3995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF", 16)
G_2048 = 2


def dh_par_de_chaves(p=P_2048, g=G_2048):
    privada = secrets.randbelow(p - 3) + 2       # 2 <= privada <= p - 2
    return privada, exp_mod(g, privada, p)


def dh_segredo(publica_do_outro, minha_privada, p=P_2048):
    if not 1 < publica_do_outro < p - 1:
        raise ValueError("chave pública inválida")
    return exp_mod(publica_do_outro, minha_privada, p)


def derivar_chave_aes(segredo, bits=256):
    # o segredo do DH é um número de 2048 bits; o AES precisa de 16/24/32 bytes.
    # Um hash (assunto das próximas missões) "espreme" o segredo no tamanho certo.
    dados = segredo.to_bytes((segredo.bit_length() + 7) // 8, "big")
    return hashlib.sha256(dados).digest()[:bits // 8]


def logaritmo_discreto(y, g, p):
    # força bruta: só funciona com p pequeno - é o que o invasor teria que fazer
    x, atual = 0, 1
    while x < p:
        if atual == y:
            return x
        atual = (atual * g) % p
        x += 1
    return None


# ---------------------------------------------------------------- envelope digital (RSA)
# o remetente sorteia a chave do AES e a "tranca" com a chave pública do
# destinatário; só a chave privada abre. É o esquema híbrido usado no TLS e no PGP.

def rsa_gerar_chaves(bits=1024, e=65537):
    while True:
        p = gerar_primo(bits // 2)
        q = gerar_primo(bits // 2)
        phi_n = (p - 1) * (q - 1)
        if p != q and coprimos(e, phi_n):
            n = p * q
            d = inverso_multiplicativo(e, phi_n)
            return (n, e), (n, d)


def envelope_fechar(chave_aes, publica):
    # versão didática (RSA "de livro", sem o enchimento OAEP usado na prática)
    n, e = publica
    m = int.from_bytes(chave_aes, "big")
    if m >= n:
        raise ValueError("a chave precisa ser menor que n")
    return exp_mod(m, e, n)


def envelope_abrir(envelope, privada, tamanho_chave):
    n, d = privada
    return exp_mod(envelope, d, n).to_bytes(tamanho_chave, "big")
