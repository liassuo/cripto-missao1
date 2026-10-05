import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from securedocs_classica import substituicao
from securedocs_classica.alfabeto import ALFABETO
from textos import MENSAGEM


def main():
    print("=== 3. SUBSTITUIÇÃO MONOALFABÉTICA ===\n")
    print("cada letra vira outra, seguindo uma permutação do alfabeto (a chave)\n")

    chave = substituicao.chave_por_palavra("SEGURANCA")
    print("chave a partir da palavra SEGURANCA:")
    print("  claro : %s" % ALFABETO)
    print("  cifra : %s" % chave)

    cifrado = substituicao.cifrar(MENSAGEM, chave)
    print("\ntexto claro: %s" % MENSAGEM)
    print("cifrado    : %s" % cifrado)
    print("decifrado  : %s" % substituicao.decifrar(cifrado, chave))

    print("\ntambém dá para gerar a chave aleatória:")
    print("  %s" % substituicao.chave_aleatoria())
    print("\nquantidade de chaves possíveis: 26! = %d" % substituicao.tamanho_espaco_chaves())


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    palavra = ler_texto("palavra-chave (vazio = chave aleatória): ", "")
    if palavra:
        chave = substituicao.chave_por_palavra(palavra)
    else:
        chave = substituicao.chave_aleatoria()
    print("\nchave    : %s" % chave)
    cifrado = substituicao.cifrar(texto, chave)
    print("cifrado  : %s" % cifrado)
    print("decifrado: %s" % substituicao.decifrar(cifrado, chave))


if __name__ == "__main__":
    main()
