import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from securedocs_classica import fluxo
from securedocs_classica.alfabeto import so_letras
from textos import MENSAGEM


def perder_letra(texto, posicao):
    return texto[:posicao] + texto[posicao + 1:]


def main():
    print("=== 7. CIFRAS DE FLUXO ===\n")
    print("síncrona  : o fluxo de chave depende só da chave (one-time pad, gerador)")
    print("assíncrona: o fluxo de chave depende também do que já foi cifrado (autochave)\n")

    print("--- SÍNCRONA: Vernam / one-time pad (letras) ---")
    print("C = (P + K) mod 26   e   P = (C - K) mod 26")
    otp_chave = fluxo.chave_vernam(len(so_letras(MENSAGEM)))
    otp_cifrado = fluxo.vernam_cifrar(MENSAGEM, otp_chave)
    print("texto claro: %s" % so_letras(MENSAGEM))
    print("chave      : %s  (aleatória, mesmo tamanho)" % otp_chave)
    print("cifrado    : %s" % otp_cifrado)
    print("decifrado  : %s" % fluxo.vernam_decifrar(otp_cifrado, otp_chave))
    print("se a chave for realmente aleatória e usada uma vez só, é impossível quebrar")
    print("(Shannon, 1949) - mas distribuir uma chave desse tamanho é o problema")

    print("\n--- SÍNCRONA: fluxo com gerador (semente curta + XOR) ---")
    print("C = P xor K   e   P = C xor K  (cifrar e decifrar são a mesma conta)")
    semente = 40213
    print("gerador congruencial linear: x = (%d*x + %d) mod 2^31" % (fluxo.LCG_A, fluxo.LCG_C))
    print("semente (chave) = %d" % semente)
    print("fluxo de chave : %s..." % fluxo.para_hex(fluxo.gerar_fluxo(semente, 12)))
    cifrado = fluxo.cifrar(MENSAGEM, semente)
    print("cifrado (hex)  : %s" % fluxo.para_hex(cifrado))
    print("decifrado      : %s" % fluxo.decifrar(cifrado, semente))

    print("\n--- ASSÍNCRONA: autochave ---")
    palavra = "SEGREDO"
    print("a chave começa com %s e continua com o próprio cifrado: K(i) = C(i - %d)"
          % (palavra, len(palavra)))
    cifrado = fluxo.autochave_cifrar(MENSAGEM, palavra)
    print("texto claro: %s" % so_letras(MENSAGEM))
    print("chave      : %s" % fluxo.fluxo_autochave(cifrado, palavra))
    print("cifrado    : %s" % cifrado)
    print("decifrado  : %s" % fluxo.autochave_decifrar(cifrado, palavra))

    print("\n--- e se uma letra do cifrado se perder no caminho? (posição 10) ---")
    print("síncrona  : %s" % fluxo.vernam_decifrar(perder_letra(otp_cifrado, 10), otp_chave))
    print("            tudo depois da letra perdida sai errado (perdeu a sincronia)")
    print("assíncrona: %s" % fluxo.autochave_decifrar(perder_letra(cifrado, 10), palavra))
    print("            só %d letras saem erradas, depois a decifragem se acerta sozinha"
          % len(palavra))


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    semente = ler_int("semente (0 a 65535): ", 0, 65535)
    cifrado = fluxo.cifrar(texto, semente)
    print("\nsíncrona (gerador)")
    print("cifrado (hex): %s" % fluxo.para_hex(cifrado))
    print("decifrado    : %s" % fluxo.decifrar(cifrado, semente))

    palavra = ler_texto("\npalavra-chave da autochave: ", "SEGREDO")
    cifrado = fluxo.autochave_cifrar(texto, palavra)
    print("\nassíncrona (autochave)")
    print("chave        : %s" % fluxo.fluxo_autochave(cifrado, palavra))
    print("cifrado      : %s" % cifrado)
    print("decifrado    : %s" % fluxo.autochave_decifrar(cifrado, palavra))


if __name__ == "__main__":
    main()
