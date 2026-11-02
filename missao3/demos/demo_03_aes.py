import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from securedocs_simetrica import aes, modos, vetores
from securedocs_simetrica.blocos import para_hex, de_hex
from textos import MENSAGEM, CHAVE_AES


def mostrar_matrizes(titulos, estados):
    linhas = [aes.matriz(e) for e in estados]
    print("    ".join("%-11s" % t for t in titulos))
    for r in range(4):
        print("    ".join(m[r] for m in linhas))


def mostrar_rodadas(bloco, chave):
    cifra = aes.Cifra(chave)
    print("%s: %d rodadas, %d chaves de rodada de 16 bytes" % (cifra.nome, cifra.rodadas,
                                                              len(cifra.chaves)))
    passos = []
    cifrado = cifra.cifrar_bloco(bloco, passos)

    print("\nestado inicial (o bloco vira uma matriz 4x4, preenchida por colunas):")
    mostrar_matrizes(["entrada", "+ chave 0"], [bloco, passos[0][2]])

    print("\nrodada 1:")
    etapas = [p for p in passos if p[0] == 1]
    mostrar_matrizes([e[1] for e in etapas], [e[2] for e in etapas])

    print("\nfim de cada rodada:")
    for rodada, etapa, estado in passos:
        if etapa == "AddRoundKey" and rodada > 0:
            print("  rodada %2d: %s" % (rodada, para_hex(estado, 4)))
    print("  (a última rodada não tem MixColumns)")

    print("\ncifrado  : %s" % para_hex(cifrado, 4))
    print("decifrado: %s" % para_hex(cifra.decifrar_bloco(cifrado), 4))
    return cifra


def main():
    print("=== 3. AES (Advanced Encryption Standard) ===\n")
    print("rede de substituição-permutação: bloco de 128 bits, chave de 128/192/256 bits")
    print("cada rodada: SubBytes -> ShiftRows -> MixColumns -> AddRoundKey\n")

    print("a S-box é calculada, não copiada: inverso em GF(2^8) + transformação afim")
    x = 0x53
    inv = aes.inverso_gf(x)
    print("  inverso de 53 em GF(2^8) = 53^254 = %02X  (confere: 53 * %02X = %02X)"
          % (inv, inv, aes.mult_gf(x, inv)))
    print("  S-box[53] = afim(%02X) = %02X" % (inv, aes.SBOX[x]))
    print("  primeira linha da S-box: " + " ".join("%02X" % b for b in aes.SBOX[:16]))
    print("  (mesma ideia do inverso multiplicativo da Missão 1, só que no corpo GF(2^8))\n")

    cifra = mostrar_rodadas(de_hex("00112233445566778899AABBCCDDEEFF"),
                            de_hex(CHAVE_AES[:32]))

    print("\nvetores de teste do FIPS 197:")
    for nome, chave, claro, esperado, obtido, fonte, ok in vetores.conferir("AES"):
        print("  %-8s %-14s -> %s  %s" % (nome, fonte, obtido, "OK" if ok else "ERRO"))

    print("\na mensagem inteira (AES-256 em CBC):")
    cifra = aes.Cifra(de_hex(CHAVE_AES))
    iv, cifrado = modos.cifrar_cbc(cifra, MENSAGEM.encode("utf-8"))
    print("  cifrado  : %s" % para_hex(cifrado, 16))
    print("  decifrado: %s" % modos.decifrar_cbc(cifra, cifrado, iv).decode("utf-8"))


def interativo():
    texto = ler_texto("bloco (até 16 caracteres): ", "SECUREDOCS 2026!")
    bloco = texto.encode("utf-8")[:16].ljust(16, b" ")
    senha = ler_texto("chave (16, 24 ou 32 caracteres): ", "TECHSECURE-CHAVE")
    chave = senha.encode("utf-8")
    if len(chave) not in aes.RODADAS:
        chave = chave[:32].ljust(16 if len(chave) <= 16 else 24 if len(chave) <= 24 else 32, b"0")
        print("  (ajustada para %d bytes: %s)" % (len(chave), chave.decode("utf-8", "replace")))
    print()
    mostrar_rodadas(bloco, chave)


if __name__ == "__main__":
    main()
