# Vetores de teste oficiais: se a implementação bate com eles, ela está correta.

from . import des, aes, rc5
from .blocos import de_hex

VETORES = [
    # nome, construtor, chave, texto claro, cifrado esperado, fonte
    ("DES", des.Cifra, "133457799BBCDFF1", "0123456789ABCDEF", "85E813540F0AB405",
     "exemplo clássico de Grabbe / Stallings"),
    ("DES", des.Cifra, "0E329232EA6D0D73", "8787878787878787", "0000000000000000",
     "Stallings"),
    ("RC5-32/12/16", rc5.Cifra, "00000000000000000000000000000000", "0000000000000000",
     "21A5DBEE154B8F6D", "Rivest (1994)"),
    ("RC5-32/12/16", rc5.Cifra, "915F4619BE41B2516355A50110A9CE91", "21A5DBEE154B8F6D",
     "F7C013AC5B2B8952", "Rivest (1994)"),
    ("AES-128", aes.Cifra, "000102030405060708090A0B0C0D0E0F",
     "00112233445566778899AABBCCDDEEFF", "69C4E0D86A7B0430D8CDB78070B4C55A", "FIPS 197, C.1"),
    ("AES-128", aes.Cifra, "2B7E151628AED2A6ABF7158809CF4F3C",
     "3243F6A8885A308D313198A2E0370734", "3925841D02DC09FBDC118597196A0B32", "FIPS 197, B"),
    ("AES-192", aes.Cifra, "000102030405060708090A0B0C0D0E0F1011121314151617",
     "00112233445566778899AABBCCDDEEFF", "DDA97CA4864CDFE06EAF70A0EC0D7191", "FIPS 197, C.2"),
    ("AES-256", aes.Cifra, "000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F",
     "00112233445566778899AABBCCDDEEFF", "8EA2B7CA516745BFEAFC49904B496089", "FIPS 197, C.3"),
]


def conferir(filtro=None):
    resultados = []
    for nome, construtor, chave, claro, esperado, fonte in VETORES:
        if filtro and not nome.startswith(filtro):
            continue
        cifra = construtor(de_hex(chave))
        obtido = cifra.cifrar_bloco(de_hex(claro))
        volta = cifra.decifrar_bloco(obtido)
        ok = obtido == de_hex(esperado) and volta == de_hex(claro)
        resultados.append((nome, chave, claro, esperado, obtido.hex().upper(), fonte, ok))
    return resultados
