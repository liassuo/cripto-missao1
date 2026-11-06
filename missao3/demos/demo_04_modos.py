import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from securedocs_simetrica import aes, modos
from securedocs_simetrica.blocos import para_hex, de_hex, dividir_blocos
from textos import CHAVE_AES


def comparar(texto, cifra):
    dados = texto.encode("utf-8")
    print("texto (%d bytes, em blocos de 16):" % len(dados))
    for b in dividir_blocos(dados, 16):
        print("  %r" % b.decode("utf-8", "replace"))

    ecb = modos.cifrar_ecb(cifra, dados)
    iv, cbc = modos.cifrar_cbc(cifra, dados)
    nonce, ctr = modos.cifrar_ctr(cifra, dados)

    for nome, cifrado in (("ECB", ecb), ("CBC", cbc), ("CTR", ctr)):
        blocos = dividir_blocos(cifrado, 16)
        repetidos = len(blocos) - len(set(blocos))
        print("\n%s (%d bytes, %d blocos repetidos):" % (nome, len(cifrado), repetidos))
        for b in blocos:
            print("  %s" % para_hex(b))

    print("\ndecifrando:")
    print("  ECB: %s" % modos.decifrar_ecb(cifra, ecb).decode("utf-8"))
    print("  CBC: %s" % modos.decifrar_cbc(cifra, cbc, iv).decode("utf-8"))
    print("  CTR: %s" % modos.decifrar_ctr(cifra, ctr, nonce).decode("utf-8"))


def main():
    print("=== 4. MODOS DE OPERAÇÃO ===\n")
    print("o AES só cifra 16 bytes; o modo diz como cifrar um arquivo inteiro")
    print("  ECB: cada bloco sozinho              C(i) = E(P(i))")
    print("  CBC: encadeia com o anterior         C(i) = E(P(i) xor C(i-1)), C(0) = IV")
    print("  CTR: vira cifra de fluxo (Missão 2)  C(i) = P(i) xor E(nonce || i)\n")

    cifra = aes.Cifra(de_hex(CHAVE_AES))
    # 3 blocos iguais, como num relatório com cabeçalhos repetidos
    texto = "SALDO: R$ 1.000 " * 3 + "CONTA 4521-7"
    comparar(texto, cifra)

    print("\nno ECB os 3 blocos iguais saem iguais: o invasor vê o padrão do documento")
    print("sem saber a chave. Por isso o SecureDocs usa CBC (com IV aleatório).")

    print("\ncifrando o MESMO texto duas vezes (com a mensagem \"SIM\"):")
    print("  ECB: %s / %s" % (para_hex(modos.cifrar_ecb(cifra, b"SIM")),
                              para_hex(modos.cifrar_ecb(cifra, b"SIM"))))
    print("  CBC: %s / %s" % (para_hex(modos.cifrar_cbc(cifra, b"SIM")[1]),
                              para_hex(modos.cifrar_cbc(cifra, b"SIM")[1])))


def interativo():
    texto = ler_texto("texto (repita trechos de 16 letras para ver o ECB vazar): ",
                      "ABCDEFGHIJKLMNOP" * 3)
    print()
    comparar(texto, aes.Cifra(de_hex(CHAVE_AES)))


if __name__ == "__main__":
    main()
