import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from securedocs_classica import fluxo
from securedocs_classica.alfabeto import so_letras
from textos import MENSAGEM


def main():
    print("=== 7. CIFRAS DE FLUXO ===\n")

    print("--- Vernam / one-time pad (letras) ---")
    chave = fluxo.chave_vernam(len(so_letras(MENSAGEM)))
    cifrado = fluxo.vernam_cifrar(MENSAGEM, chave)
    print("texto claro: %s" % so_letras(MENSAGEM))
    print("chave      : %s  (aleatória, mesmo tamanho)" % chave)
    print("cifrado    : %s" % cifrado)
    print("decifrado  : %s" % fluxo.vernam_decifrar(cifrado, chave))
    print("se a chave for realmente aleatória e usada uma vez só, é impossível quebrar")
    print("(Shannon, 1949) - mas distribuir uma chave desse tamanho é o problema")

    print("\n--- fluxo com gerador (semente curta + XOR) ---")
    semente = 40213
    print("gerador congruencial linear: x = (%d*x + %d) mod 2^31" % (fluxo.LCG_A, fluxo.LCG_C))
    print("semente (chave) = %d" % semente)
    print("fluxo de chave : %s..." % fluxo.para_hex(fluxo.gerar_fluxo(semente, 12)))
    cifrado = fluxo.cifrar(MENSAGEM, semente)
    print("cifrado (hex)  : %s" % fluxo.para_hex(cifrado))
    print("decifrado      : %s" % fluxo.decifrar(cifrado, semente))


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    semente = ler_int("semente (0 a 65535): ", 0, 65535)
    cifrado = fluxo.cifrar(texto, semente)
    print("\ncifrado (hex): %s" % fluxo.para_hex(cifrado))
    print("decifrado    : %s" % fluxo.decifrar(cifrado, semente))


if __name__ == "__main__":
    main()
