import secrets


def chave_aleatoria(n_bytes):
    # secrets usa o gerador do sistema operacional (não é previsível como o random)
    return secrets.token_bytes(n_bytes)


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def para_hex(dados, grupo=0):
    texto = dados.hex().upper()
    if not grupo:
        return texto
    return " ".join(texto[i:i + 2 * grupo] for i in range(0, len(texto), 2 * grupo))


def de_hex(texto):
    return bytes.fromhex("".join(texto.split()))


def bytes_para_int(dados):
    return int.from_bytes(dados, "big")


def int_para_bytes(x, n_bytes):
    return x.to_bytes(n_bytes, "big")


def dividir_blocos(dados, tamanho):
    return [dados[i:i + tamanho] for i in range(0, len(dados), tamanho)]


# PKCS#7: completa o último bloco com n bytes de valor n (sempre acrescenta,
# então quando o tamanho já é múltiplo do bloco entra um bloco inteiro de enchimento)
def pkcs7_preencher(dados, tamanho_bloco):
    n = tamanho_bloco - len(dados) % tamanho_bloco
    return dados + bytes([n]) * n


def pkcs7_remover(dados, tamanho_bloco):
    if not dados or len(dados) % tamanho_bloco != 0:
        raise ValueError("tamanho do cifrado não é múltiplo do bloco")
    n = dados[-1]
    if n < 1 or n > tamanho_bloco or dados[-n:] != bytes([n]) * n:
        raise ValueError("enchimento inválido (chave errada ou arquivo alterado)")
    return dados[:-n]


def bits_diferentes(a, b):
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


def inverter_bit(dados, posicao):
    # posição 0 = bit mais significativo do primeiro byte
    saida = bytearray(dados)
    saida[posicao // 8] ^= 0x80 >> (posicao % 8)
    return bytes(saida)
