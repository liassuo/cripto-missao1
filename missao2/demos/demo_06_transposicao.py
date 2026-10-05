import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from securedocs_classica import transposicao
from textos import MENSAGEM


def main():
    print("=== 6. TRANSPOSIÇÃO ===\n")
    print("as letras não mudam, só trocam de lugar\n")

    palavra = "CHAVE"
    print("transposição colunar com a palavra %s" % palavra)
    ordem = transposicao.ordem_colunas(palavra)
    print("  ordem de leitura das colunas (alfabética): %s" % [palavra[i] for i in ordem])
    print("  " + "  ".join(palavra))
    for linha in transposicao.grade(MENSAGEM, palavra):
        print("  " + "  ".join(linha))
    cifrado = transposicao.cifrar(MENSAGEM, palavra)
    print("\ntexto claro: %s" % MENSAGEM)
    print("cifrado    : %s" % cifrado)
    print("decifrado  : %s" % transposicao.decifrar(cifrado, palavra))

    print("\ncerca de trilhos (zigue-zague) com 3 trilhos:")
    cerca = transposicao.cerca_cifrar(MENSAGEM, 3)
    print("cifrado    : %s" % cerca)
    print("decifrado  : %s" % transposicao.cerca_decifrar(cerca, 3))


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    palavra = ler_texto("palavra-chave (colunar): ", "CHAVE")
    cifrado = transposicao.cifrar(texto, palavra)
    print("\ncolunar   : %s" % cifrado)
    print("decifrado : %s" % transposicao.decifrar(cifrado, palavra))
    trilhos = ler_int("\nnúmero de trilhos (cerca): ", 2, 20)
    cerca = transposicao.cerca_cifrar(texto, trilhos)
    print("cerca     : %s" % cerca)
    print("decifrado : %s" % transposicao.cerca_decifrar(cerca, trilhos))


if __name__ == "__main__":
    main()
