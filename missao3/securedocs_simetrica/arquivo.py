# Experimento da missão: arquivo original -> AES -> arquivo cifrado -> AES -> arquivo original
# Formato do arquivo cifrado (.sdoc):
#   "SDOC" | versão (1 byte) | tamanho da chave (1 byte) | IV (16 bytes) | cifrado (AES-CBC + PKCS#7)

import os

from . import aes, modos
from .blocos import chave_aleatoria, para_hex, de_hex

ASSINATURA = b"SDOC"
VERSAO = 1


def gerar_chave(bits=256):
    if bits not in (128, 192, 256):
        raise ValueError("o AES usa chave de 128, 192 ou 256 bits")
    return chave_aleatoria(bits // 8)


def salvar_chave(caminho, chave):
    with open(caminho, "w") as f:
        f.write(para_hex(chave) + "\n")


def ler_chave(caminho):
    with open(caminho) as f:
        return de_hex(f.read())


def cifrar_dados(dados, chave, iv=None):
    iv, cifrado = modos.cifrar_cbc(aes.Cifra(chave), dados, iv)
    return ASSINATURA + bytes([VERSAO, len(chave)]) + iv + cifrado


def decifrar_dados(conteudo, chave):
    if conteudo[:4] != ASSINATURA:
        raise ValueError("não é um arquivo cifrado pelo SecureDocs")
    if conteudo[4] != VERSAO:
        raise ValueError("versão de arquivo desconhecida: %d" % conteudo[4])
    if conteudo[5] != len(chave):
        raise ValueError("o arquivo foi cifrado com chave de %d bits, a informada tem %d"
                         % (8 * conteudo[5], 8 * len(chave)))
    iv, cifrado = conteudo[6:22], conteudo[22:]
    return modos.decifrar_cbc(aes.Cifra(chave), cifrado, iv)


def cifrar_arquivo(origem, destino, chave):
    with open(origem, "rb") as f:
        dados = f.read()
    conteudo = cifrar_dados(dados, chave)
    with open(destino, "wb") as f:
        f.write(conteudo)
    return len(dados), len(conteudo)


def decifrar_arquivo(origem, destino, chave):
    with open(origem, "rb") as f:
        conteudo = f.read()
    dados = decifrar_dados(conteudo, chave)
    with open(destino, "wb") as f:
        f.write(dados)
    return len(conteudo), len(dados)


def arquivos_iguais(a, b):
    if os.path.getsize(a) != os.path.getsize(b):
        return False
    with open(a, "rb") as fa, open(b, "rb") as fb:
        return fa.read() == fb.read()
