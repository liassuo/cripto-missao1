import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from securedocs_classica import vigenere
from textos import MENSAGEM


def main():
    print("=== 4. CIFRA DE VIGENÈRE ===\n")
    print("C_i = (P_i + K_(i mod m)) mod 26  -> cada posição usa um César diferente\n")

    for linha in vigenere.tabela_passos(MENSAGEM, "SEGREDO"):
        print(linha)
    cifrado = vigenere.cifrar(MENSAGEM, "SEGREDO")
    print("\ncifrado  : %s" % cifrado)
    print("decifrado: %s" % vigenere.decifrar(cifrado, "SEGREDO"))
    print("\nrepare: os três R de TRANSFERIR viraram V, J e X")


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    chave = ler_texto("chave: ", "SEGREDO")
    cifrado = vigenere.cifrar(texto, chave)
    print()
    for linha in vigenere.tabela_passos(texto, chave):
        print(linha)
    print("\ncifrado  : %s" % cifrado)
    print("decifrado: %s" % vigenere.decifrar(cifrado, chave))


if __name__ == "__main__":
    main()
